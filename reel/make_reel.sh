#!/usr/bin/env bash
# Збирає рілс у стилі «Збери рілс з рандомних відео цього року».
#
# Використання:
#   ./make_reel.sh <папка_з_кліпами> [вихід.mp4] [музика.mp3]
#
# Змінні (необов'язково):
#   TITLE_TOP="Новий тренд:"  TITLE="Збери рілс з рандомних відео цього року"
#   INTRO=5.7   CUT=1.1   (тривалість інтро та кожного наступного кліпу, сек)
#   LYRICS=lyrics.txt  (рядки "початок|кінець|English|Українською")
#
# Кліпи беруться в алфавітному порядку (назвіть 01.mp4, 02.mp4 ...).
# Перший кліп стає інтро із заголовком. Підтримуються і фото (jpg/png/heic->jpg).
set -euo pipefail

SRC="${1:?Вкажіть папку з кліпами}"
OUT="${2:-reel.mp4}"
MUSIC="${3:-}"
TITLE_TOP="${TITLE_TOP:-Новий тренд:}"
TITLE="${TITLE:-Збери рілс з рандомних відео цього року}"
INTRO="${INTRO:-5.7}"
CUT="${CUT:-1.1}"
LYRICS="${LYRICS:-}"
FONT_SERIF="${FONT_SERIF:-/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf}"
FONT_SANS="${FONT_SANS:-/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf}"
W=1080; H=1920; FPS=30

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
LOOK="scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},setsar=1,fps=${FPS},eq=contrast=1.06:saturation=1.12:brightness=0.01,vignette=PI/5,format=yuv420p"

# Ділимо заголовок на 2 рядки приблизно навпіл
split_title() {
  python3 -c 'import sys
w=sys.argv[1].split(); best=None
for i in range(1,len(w)):
  a=" ".join(w[:i]); b=" ".join(w[i:])
  d=abs(len(a)-len(b))
  if best is None or d<best[0]: best=(d," ".join(w[:i]),b)
print(best[1] if best else sys.argv[1]); print(best[2] if best else "")' "$1"
}
mapfile -t TL < <(split_title "$TITLE")
printf '%s' "$TITLE_TOP" > "$TMP/t0.txt"; printf '%s' "${TL[0]}" > "$TMP/t1.txt"; printf '%s' "${TL[1]:-}" > "$TMP/t2.txt"

mapfile -t FILES < <(find "$SRC" -maxdepth 1 -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.m4v' -o -iname '*.webm' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) | sort)
[ "${#FILES[@]}" -gt 0 ] || { echo "У папці немає відео/фото"; exit 1; }
echo "Знайдено кліпів: ${#FILES[@]}"

i=0; : > "$TMP/list.txt"
for f in "${FILES[@]}"; do
  i=$((i+1)); n=$(printf '%03d' "$i")
  dur="$CUT"; [ "$i" -eq 1 ] && dur="$INTRO"
  vf="$LOOK"
  if [ "$i" -eq 1 ]; then
    sh='shadowcolor=black@0.45:shadowx=2:shadowy=2'
    vf="$vf,drawtext=fontfile=$FONT_SERIF:textfile=$TMP/t0.txt:fontsize=44:fontcolor=white:$sh:x=(w-text_w)/2:y=170,drawtext=fontfile=$FONT_SERIF:textfile=$TMP/t1.txt:fontsize=72:fontcolor=white:$sh:x=(w-text_w)/2:y=240,drawtext=fontfile=$FONT_SERIF:textfile=$TMP/t2.txt:fontsize=72:fontcolor=white:$sh:x=(w-text_w)/2:y=330"
  fi
  case "${f,,}" in
    *.jpg|*.jpeg|*.png)
      # фото: легкий наїзд камери
      frames=$(python3 -c "print(round($dur*$FPS))")
      ffmpeg -v error -y -loop 1 -i "$f" -t "$dur" -vf "scale=${W}*2:${H}*2:force_original_aspect_ratio=increase,crop=${W}*2:${H}*2,zoompan=z='1+0.06*on/$frames':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=$frames:s=${W}x${H}:fps=$FPS,$vf" -an -c:v libx264 -preset veryfast -crf 19 "$TMP/$n.mp4" ;;
    *)
      len=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
      # беремо шматок із середини кліпу
      ss=$(python3 -c "l=float('$len'); d=float('$dur'); print(max(0.0,(l-d)/2))")
      ffmpeg -v error -y -ss "$ss" -i "$f" -t "$dur" -vf "$vf" -an -c:v libx264 -preset veryfast -crf 19 "$TMP/$n.mp4" ;;
  esac
  echo "file '$TMP/$n.mp4'" >> "$TMP/list.txt"
  printf '\r  оброблено %d/%d' "$i" "${#FILES[@]}"
done; echo

ffmpeg -v error -y -f concat -safe 0 -i "$TMP/list.txt" -c copy "$TMP/joined.mp4"
TOTAL=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP/joined.mp4")

# Субтитри пісні (англ. великим, укр. дрібніше під ним), як у оригіналі
SUBVF="null"
if [ -n "$LYRICS" ] && [ -f "$LYRICS" ]; then
  SUBVF=""; k=0
  while IFS='|' read -r a b en ua; do
    [ -z "${a// }" ] && continue; k=$((k+1))
    printf '%s' "$en" > "$TMP/en$k.txt"; printf '%s' "$ua" > "$TMP/ua$k.txt"
    en_q="enable='between(t,$a,$b)'"
    SUBVF+="drawtext=fontfile=$FONT_SANS:textfile=$TMP/en$k.txt:fontsize=46:fontcolor=white:borderw=2:bordercolor=black@0.35:x=(w-text_w)/2:y=h*0.79:$en_q,"
    SUBVF+="drawtext=fontfile=$FONT_SANS:textfile=$TMP/ua$k.txt:fontsize=34:fontcolor=white:borderw=2:bordercolor=black@0.35:x=(w-text_w)/2:y=h*0.79+62:$en_q,"
  done < "$LYRICS"
  SUBVF="${SUBVF%,}"
fi

if [ -n "$MUSIC" ]; then
  ffmpeg -v error -y -i "$TMP/joined.mp4" -i "$MUSIC" -vf "$SUBVF" -map 0:v -map 1:a -af "afade=t=out:st=$(python3 -c "print(max(0,$TOTAL-1.5))"):d=1.5" -t "$TOTAL" -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -movflags +faststart "$OUT"
else
  ffmpeg -v error -y -i "$TMP/joined.mp4" -vf "$SUBVF" -c:v libx264 -preset medium -crf 18 -movflags +faststart "$OUT"
fi
echo "Готово: $OUT ($(printf '%.1f' "$TOTAL") с)"

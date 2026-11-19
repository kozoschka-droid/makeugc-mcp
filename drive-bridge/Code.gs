/**
 * Drive Bridge для Claude: завантаження й скачування відео в папці "Shop Content".
 *
 * Встановлення (≈3 хв):
 * 1. https://script.google.com → New project → вставити цей код замість усього.
 * 2. Вписати свій KEY нижче (будь-який довгий випадковий рядок; той самий
 *    записати в Google Doc "05_brand/Drive Bridge").
 * 3. Deploy → New deployment → тип "Web app":
 *      Execute as: Me
 *      Who has access: Anyone
 *    → Deploy → дозволити доступ до Google Drive → скопіювати Web app URL
 *    у той самий Doc "05_brand/Drive Bridge".
 *
 * Скрипт працює лише з файлами всередині папки ROOT_ID і лише з правильним KEY.
 */
const ROOT_ID = '14jdR1pSIRt19Tc_nxX1RT9kNCGEYGEBA'; // Shop Content
const KEY = 'ВСТАВТЕ_КЛЮЧ_СЮДИ';

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function insideRoot_(fileOrFolder) {
  if (fileOrFolder.getId() === ROOT_ID) return true;
  const seen = {};
  let parents = fileOrFolder.getParents();
  while (parents.hasNext()) {
    const p = parents.next();
    if (p.getId() === ROOT_ID) return true;
    if (seen[p.getId()]) continue;
    seen[p.getId()] = true;
    if (insideRoot_(p)) return true;
  }
  return false;
}

function doGet(e) {
  const q = e.parameter;
  if (q.key !== KEY) return json_({ error: 'bad key' });
  try {
    if (q.action === 'list') {
      const folder = DriveApp.getFolderById(q.folder || ROOT_ID);
      if (!insideRoot_(folder)) return json_({ error: 'outside root' });
      const out = [];
      const files = folder.getFiles();
      while (files.hasNext()) {
        const f = files.next();
        out.push({ id: f.getId(), name: f.getName(), mime: f.getMimeType(),
                   size: f.getSize(), modified: f.getLastUpdated() });
      }
      const subs = folder.getFolders();
      while (subs.hasNext()) {
        const s = subs.next();
        out.push({ id: s.getId(), name: s.getName(), mime: 'folder' });
      }
      return json_({ files: out });
    }
    if (q.action === 'get') {
      const f = DriveApp.getFileById(q.id);
      if (!insideRoot_(f)) return json_({ error: 'outside root' });
      return json_({ name: f.getName(), mime: f.getMimeType(),
                     data: Utilities.base64Encode(f.getBlob().getBytes()) });
    }
    return json_({ error: 'unknown action' });
  } catch (err) {
    return json_({ error: String(err) });
  }
}

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    if (body.key !== KEY) return json_({ error: 'bad key' });
    const folder = DriveApp.getFolderById(body.folder || ROOT_ID);
    if (!insideRoot_(folder)) return json_({ error: 'outside root' });
    const blob = Utilities.newBlob(Utilities.base64Decode(body.data),
                                   body.mime || 'video/mp4', body.name);
    const f = folder.createFile(blob);
    return json_({ id: f.getId(), name: f.getName(), url: f.getUrl() });
  } catch (err) {
    return json_({ error: String(err) });
  }
}

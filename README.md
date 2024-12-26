## Sửa extension:
### 1. Bị lỗi ảnh
- Phần ảnh `logo.png` ko hiện lúc cái cảnh báo hiện (ở file `content.js`)

### 2. Lỗi code
- Extension luôn hiện `This site is flagged as malicious.` ( ở file `popup.js`)

### 3. Cải tiến phần white list
- Khi nhận `URL` từ website, tách phần lấy phần `Domain` nhưng vẫn gửi `URL` về server
- Mỗi khi người dùng ấn `Process`, lưu `Domain` vào white list.
- Mỗi khi người dùng vào các `URL` khác nhưng vẫn thuộc `Domain` đấy thì chỉ cần tách phần `Domain` 
từ `URL` và so sánh nó với phần `Domain` trong white list.

### 4. Có thể cải thiện thêm phần front-end
- Cải thiện file 2 file: `popup.html`, `popup.css`
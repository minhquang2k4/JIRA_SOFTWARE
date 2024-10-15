# JIRA_SOFTWARE

Code thì tách nhánh từ nhánh dev, sau khi code xog 1 tính năng nào đó thì đẩy lên nhánh của người đó (vd dev-quang)

sau đó nhờ 1 người khác merge. lưu ý ko được tự merge để ng khác review code trước.

## Khởi tạo môi trường ảo

- Chạy lệnh tạo môi trường ảo: python -m venv .venv
- activate môi trường ảo: .venv\Scripts\activate
- Chạy lênh pip install -r requirements.txt để tải các thư viện về
- Chạy project: python app.py

## Quy trình code:

- Đứng ở nhánh dev. thực hiện pull code từ nhánh dev mới nhất về. (git pull origin dev)
- Nếu đã có nhánh của từng người thì thực hiện việc chuyển sang nhánh đó ( git checkout dev-quang ) rồi merge code từ nhánh dev. ( git merge dev )
- Bắt đầu code

## Quy trình push:

* Sau khi code xog muốn push code ta thực hiện:
* pip freeze -l > requirements.txt để cập nhật các thư viện đã tải ở môi trường hiện tại
* Chuyển sang nhánh dev. thực hiện pull (git checkout dev -> git pull origin dev)
* Chuyển sang nhánh dev-quang. thực hiện merge trước ở local (git checkout dev-quang -> git merge dev)
  * check file xem có conflict không. nếu có hãy xử lý hết conflict trước
  * thực hiện push
* Nhờ 1 người khác merge

## Cập nhập db

* Sau khi sửa hoặc thêm model chạy lệnh: flask db migrate -m "Describe your changes here"
* Sau đó: flask db upgrade

# Note: để khoảng cách tab = 2. Không để 4

from fastapi import APIRouter, Body, File, UploadFile
from pathlib import Path
import shutil
from fastapi.responses import JSONResponse, Response
from fastapi.params import Depends
from sqlalchemy import text
from sqlalchemy.orm import load_only
from .models import Item, Attachment, String, Column
from .schemas import ItemRequest, ItemDelete, DeleteItemsRequest
from .database import engine, SessionLocal, Base
from typing import List

router = APIRouter()

UPLOAD_FOLDER = Path("uploads")

# Создаем папку для загрузок, если она не существует
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@router.post("/uploadFileToLocal/")
async def upload_file(file: UploadFile = File(...)):
    # Открываем файл для записи в папку uploads с тем же именем файла
    with open(UPLOAD_FOLDER / file.filename, "wb") as buffer:
        # Копируем содержимое загруженного файла в новый файл
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}


@router.post("/upload/")
async def upload_file(files: List[UploadFile] = File(...)):
    print("2upload_file started files:", files)
    count = 0
    try:
        # Сохранение объекта в базе данных
        session = SessionLocal()

        for file in files:
            count = count + 1
            print("3upload_file file", count, file)
            print("3upload_file content_type", file.content_type)
            content_type = file.content_type
            content = await file.read()
            file_location = f"d:/files/{file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(content)
            '''    
            print("3upload_file data len", len(data))
            try:
                print("3upload_file save start")
                file_location = f"d:/files/{file.filename}"
                print("3upload_file file_location", file_location)
                with open(file_location, "wb+") as file_object:
                    file_object.write(file.file.read())
                    print("2contents save to: ", file_location)
                print("3upload_file save finish")
                contents = file.file.read()
                with open(file.filename, 'wb') as f:
                    f.write(contents)
                print("0 file.filename:", file.filename, "contents len: ", len(contents), ": ", contents)
                #  print("2contents: ", contents)
            except Exception:
                return {"message": "There was an error uploading the file(s)"}
            finally:
                file.file.close()
            print("1 file.filename:", file.filename, "contents len: ", len(contents))
            '''

            attachment = Attachment(
                name=file.filename,
                size=file.size,
                content=content,
                content_type=content_type
            )

            session.add(attachment)

        session.commit()

        # Здесь вы можете обработать загруженный файл, например, сохранить его на сервере
        # или выполнить другие действия с ним
        ''' print(f'filename>>> {file.filename}')
        print(f'file>>> {file.file}')
        return JSONResponse({"filename": file.filename}) '''
        return JSONResponse({"filename": "test", "ok": "true", "success": "true"})
    except Exception as e:
        # Обработка ошибок загрузки файла
        return print(e)


@router.post("/insert/")
async def insert_data(item_request: ItemRequest):
    item = Item(
        name=item_request.name,
        description=item_request.description,
        price=item_request.price,
        tax=item_request.tax
    )

    # Сохранение объекта в базе данных
    session = SessionLocal()
    session.add(item)
    session.commit()

    # Возврат сохраненного объекта

    return item


@router.get("/inserted/")
async def inserted():
    s = SessionLocal()
    r = s.query(Item).all()
    return r


@router.get("/attachments/")
async def get_att_all():
    s = SessionLocal()
    r = s.query(Attachment).options(load_only(Attachment.name, Attachment.size, Attachment.content_type)).all()
    return r


@router.get("/attachments/{att_id}")
async def get_att_by_id(att_id: int):
    s = SessionLocal()
    r = s.query(Attachment).filter(Attachment.id == att_id).first()
    ba: bytearray = r.content
    print("att_id", att_id, "file", r.name, "data len", len(ba))
    return Response(content=ba, media_type=r.content_type)


@router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    s = SessionLocal()
    s.query(Item).filter(Item.id == item_id).delete()
    s.commit()
    print("delete item: ", item_id)
    return


@router.delete("/delete_items/")
async def delete_items(items: DeleteItemsRequest = Body(...)):
    print("delete items: ", items.ids)
    s = SessionLocal()
    for item_id in items.ids:
        print("delete item: ", item_id)
        s.query(Item).filter(Item.id == item_id).delete()
    s.commit()
    # Здесь вы можете выполнить удаление элементов из вашей базы данных
    return {"message": "Items deleted successfully"}


'''
@router.post("/items/")
async def create_item(item: Item, db: Session = Depends(SessionLocal)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
'''

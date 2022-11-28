import uvicorn
from fastapi import FastAPI, Response, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from database_client import DatabaseClient
import os
from models.info_schema import InforData

API_KEY = "1234567asdfgh"
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


app = FastAPI()

db_client = DatabaseClient(
    user="admin",
    database="db",
    host=os.environ.get("DB_HOST", "localhost"),
    password="test",
)


@app.get("/api/{id}")
async def get_info_base_id(id:int, response: Response, api_key: APIKey = Depends(get_api_key)):
    info = db_client.get_information(id=id)
    # if returned info is not empty
    if not info:
        response.status_code = 500
        return {
            "error":"Id does not exist.",
            "code":"ID_NOT_EXIST"
        }
    else:
        return info[0]


@app.post("/api/update/{id}")
def update_info_base_id(id: int, update_data: InforData, response: Response, api_key: APIKey = Depends(get_api_key)):
    update_dict = update_data.dict()
    data_dict = dict()
    for col in update_dict.keys():
        val = update_dict[col]
        if val != "string":
            data_dict[col] = val

    if data_dict:
        update_success = db_client.update_information(id, data_dict)
        if update_success:
            return {
                "status": "ok",
                "id": id
            }
        else:
            response.status_code = 500
            return {
                "error": "Couldn't update info to database.",
                "code": "DATABASE_WRITE_ERROR"
            }
    else:
        return {
            "Nothing to update."
        }


@app.delete("/api/delete/{id}")
def delete_info_base_id(id: int, response: Response, api_key: APIKey = Depends(get_api_key)):
    rows_deleted = db_client.delete_information(id)
    # IF id is in database, and rows_deleted is 1 if delete successfully
    if rows_deleted:
        return {"status": "ok"}
    else:
        response.status_code = 500
        return {
            "error": "Couldn't delete because id is not in database.",
            "code": "ID_NOT_EXIST_ERROR"
        }


@app.get("/api/persons/emails/")
def get_persons_with_same_email(response: Response):
    persons = db_client.all_persons_with_duplicate_email()
    emails_dict = dict()
    if persons:
        for p in persons:
            first_name = p[0]
            last_name = p[1]
            email = p[2]
            name = first_name + " " + last_name
            if email not in emails_dict.keys():
                emails_dict[email] = name
            else:
                emails_dict[email] = emails_dict[email] + ", " + name

        return emails_dict
    else:
        response.status_code = 200
        return {"status": "No persons with duplicate email address"}


@app.post("/api/email/{email}")
def get_persons_by_email(email: str, response: Response, api_key: APIKey = Depends(get_api_key)):
    # return email
    persons = db_client.persons_with_same_email(email=email)
    # if returned info is not empty
    if not persons:
        response.status_code = 500
        return {
            "status": "This email is not in the database",
            "error": "EMAIL_NOT_EXIST"
        }

    if len(persons) == 1:
        return {"status": " No other persons are using this email address"}
    else:
        persons_dict = dict()
        persons_dict[email] = list()
        for p in persons:
            first_name = p[0]
            last_name = p[1]
            name = "first_name: {} last_name: {}".format(first_name, last_name)
            persons_dict[email].append(name)

        return persons_dict


if __name__ == "__main__":

    # json_file = "/Users/wen/PycharmProjects/SanomaProject/APIAssignment/database/data.json"
    # ingest_success = db_client.ingest_json(json_file)
    # if ingest_success:
    #     print("Successfully ingest the data.json into Postgresql database.")

    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")

    # di = {"first_name":"YYY","last_name":"XXX"}
    # # di = {"first_name": "QQ"}
    #
    # r = db_client.update_information(person_id='23',update_data_dict=di)
    # print(r)





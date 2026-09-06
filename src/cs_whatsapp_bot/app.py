import fastapi


app = fastapi.FastAPI()


@app.post("/reply")
async def reply():
    pass


# import os
#
# import dotenv
# import fastapi as fapi
# import httpx2
# import uvicorn
#
# from fastapi import responses as resp
#
#
# dotenv.load_dotenv()
#
# VERIFY_TOKEN = "cs_whatsapp_token"
#
# app = fapi.FastAPI()
#
#
# @app.get("/webhook")
# async def verify_webhook(request: fapi.Request) -> Response:
#     params = request.query_params
#     token = params.get("hub.verify_token")
#     challenge = params.get("hub.challenge")
#
#     if token == VERIFY_TOKEN:
#         return resp.PlainTextResponse(challenge)
#
#     return fapi.Response("Forbidden", status_code=403)
#
# @app.post("/webhook")
# async def receive_webhook(request: fapi.Request) -> None:
#     data = await request.json()
#     print(data)
#
#     access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
#     phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
#     recipient = os.getenv("WHATSAPP_RECIPIENT")
#
#     url = f"https://graph.facebook.com/v26.0/{phone_number_id}/messages"
#
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json",
#     }
#
#     data = {
#         "messaging_product": "whatsapp",
#         "recipient_type": "individual",
#         "to": recipient,
#         "type": "text",
#         "text": {
#             "preview_url": False,
#             "body": "Здравствуйте! Заполните пожалуйста анкету:"
#         },
#     }
#
#     response = httpx2.post(
#         url,
#         headers=headers,
#         json=data,
#     )
#
#     print(response.status_code)
#     print(response.json())
#
#     return {"status": "OK"}
#
#
# if __name__ == "__main__":
#     uvicorn.run(app)

from fastapi import FastAPI

from app.routers.equipment import router

app = FastAPI(title="기업 IT 자산 지급 가능 여부 API")
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}

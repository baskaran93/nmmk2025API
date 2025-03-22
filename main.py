from fastapi import FastAPI
from src.apis.User import router as user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # ✅ Allow all headers
)

app.include_router(user)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000, reload=True)

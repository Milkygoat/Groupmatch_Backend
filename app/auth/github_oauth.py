import httpx
# import requests

from app.core.config import settings

# ------------------------------------------------------
# STEP 1 : Generate Login URL
# ------------------------------------------------------
def generate_github_login_url():
    return (
        "https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={settings.GITHUB_REDIRECT_URI}"
        "&scope=user:email"
    )


# ------------------------------------------------------
# STEP 2 : Exchange CODE ➜ ACCESS TOKEN
# ------------------------------------------------------
async def get_github_access_token(code: str):
    url = "https://github.com/login/oauth/access_token"

    data = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.GITHUB_REDIRECT_URI
    }

    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, headers=headers)
        return response.json()


# ------------------------------------------------------
# STEP 3 : Get user info from GitHub
# ------------------------------------------------------
async def get_github_user(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        res1 = await client.get("https://api.github.com/user", headers=headers)
        res2 = await client.get("https://api.github.com/user/emails", headers=headers)

    user_data = res1.json()
    email_data = res2.json()

    # email utama
    primary_email = email_data[0]["email"] if email_data else None

    return {
        "email": primary_email,
        "name": user_data.get("name") or user_data.get("login"),
        "username": user_data.get("login"),
        "picture": user_data.get("avatar_url")
    }


import pytest
from models import User
from auth import create_access_token
from unittest.mock import patch
from sqlalchemy import select

# LOGIN ROUTE
@pytest.mark.asyncio
async def test_login(client, test_user):

  response = await client.post("/api/users/login", data={
    "username": test_user.email,
    "password": "101010"
  })


  assert response.status_code == 200
  assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client, test_user):

  response = await client.post("/api/users/login", data={
    "username": test_user.email,
    "password": "101011"
  })


  assert response.status_code == 401
  assert response.json()["detail"] == "Invalid Credentials"

@pytest.mark.asyncio
async def test_login_user_not_exist(client):

  response = await client.post("/api/users/login", data={
    "username": "aremu@gmail.com",
    "password": "101010"
  })


  assert response.status_code == 401
  assert response.json()["detail"] == "Invalid Credentials"

@pytest.mark.asyncio
async def test_login_case_insensitive(client, test_user):

  response = await client.post("/api/users/login", data={
    "username": test_user.email.upper(),
    "password": "101010"
  })


  assert response.status_code == 200
  assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_missing_password(client):

  response = await client.post("/api/users/login", data={
    "username": "opeyemi@gmail.com"
  })

  assert response.status_code == 422
 
# CREATE USER ROUTE
@pytest.mark.asyncio
async def test_create_user(client):

  response = await client.post(f"/api/users/register", json={
    "username": "Abdulsalam",
    "email": "abdu@gmail.com",
    "password": "202020"
  })

  assert response.status_code == 201
  data = response.json()
  assert data["username"] == "Abdulsalam"
  assert data["email"] == "abdu@gmail.com"


@pytest.mark.asyncio
async def test_existing_username(client, test_user):

  response = await client.post(f"/api/users/register", json={
    "username": "opeyemi",
    "email": "opeyemi@gmail.com",
    "password": "202020"
  })

  assert response.status_code == 400
  assert response.json() == {
    "detail": "username already exist"
  }

@pytest.mark.asyncio
async def test_existing_email(client, test_user):

  response = await client.post(f"/api/users/register", json={
    "username": "opeyemi2",
    "email": "opeyemi@gmail.com",
    "password": "202020"
  })

  assert response.status_code == 400
  assert response.json() == {
    "detail": "email already exist"
  }


# UPDATE USER ROUTE

@pytest.mark.asyncio
async def test_update_user(client, test_user, auth_header):

  response = await client.patch(
    f"/api/users/{test_user.id}",
    headers=auth_header,
    json={
      "username": "opeyemi100"
    }
    )
  
  assert response.status_code == 200
  assert response.json()["username"] == "opeyemi100"
  assert response.json()["email"] == "opeyemi@gmail.com"

@pytest.mark.asyncio
async def test_update_user_not_authorized(client, auth_header):

  response = await client.patch(
    "/api/users/2",
    headers=auth_header,
    json={
      "username": "opeyemi100"
    }
    )
  
  assert response.status_code == 403
  assert response.json() == {
    "detail": "Not authorized to update this user"
  }


@pytest.mark.asyncio
async def test_update_user_email_already_exist(client, db_session, test_user):

  new_user = User(
    username="aremu",
    email="aremu@gmail.com",
    passwordhash="101010"
  )

  db_session.add(new_user)
  await db_session.commit()
  await db_session.refresh(new_user)

  token = create_access_token({
    "sub": str(new_user.id)
  })

  response = await client.patch(
    f"/api/users/{new_user.id}",
    headers={
      "Authorization": f"Bearer {token}"
    },
    json={
      "email": "opeyemi@gmail.com"
    }
  )


  assert response.status_code == 400
  assert response.json()["detail"] == "email already exist"


# DELETE ROUTE
@pytest.mark.asyncio
async def test_delete_user(client, test_user, auth_header, db_session):

  with patch("Router.users.delete_profile_picture") as delete_profile:

    resposne = await client.delete(
      f"/api/users/{test_user.id}",
      headers=auth_header
      )
    

    assert resposne.status_code == 204
    delete_profile.assert_called_once_with(test_user.image_file)

  stmt = await db_session.execute(
    select(User)
    .where(User.id == test_user.id)
  )

  assert stmt.scalar_one_or_none() is None


# GET ALL USERS POST ROUTE
@pytest.mark.asyncio
async def test_all_user_post(client, test_user, test_post):

  response = await client.get(f"/api/users/{test_user.id}/posts")

  assert response.status_code == 200
  data = response.json()
  assert data[0]["title"] == "Test post"
  assert data[0]["to_user"]["username"] == test_user.username

















  

# GET USER ROUTE
@pytest.mark.asyncio
async def test_get_user(client, test_user):

  response = await client.get(f"/api/users/{test_user.id}")

  assert response.status_code == 200
  data = response.json()

  assert data["id"] == test_user.id
  assert data["username"] == "opeyemi"
  
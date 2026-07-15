import pytest


@pytest.mark.asyncio
async def test_create_post(client, auth_header):

  response = await client.post(
    "/api/posts", 
    json= {
      "title": "love",
      "content": "testing is hard"
    },
    headers=auth_header
    )
  

  assert response.status_code == 201
  data = response.json()
  assert data["title"] == "love"
  assert data["content"] == "testing is hard"
  assert data["to_user"]["username"] == "opeyemi"




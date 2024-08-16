from fastapi import APIRouter, Request, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from bson import ObjectId
from bson.json_util import dumps
import json

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    template = request.state.templates.get_template(
        "./flashcards/flashcards_homepage.html")
    return template.render(request=request)


@router.get('/{collection_name}', response_class=HTMLResponse)
async def get_flashcards(collection_name: str, request: Request):
    try:
        print(f'collection_name: {collection_name}')

        # Fetch the cursor for the collection
        cursor = request.app.mongodb.flashcard[collection_name].find()

        # Use async for to iterate over the cursor
        flashcards = []
        async for card in cursor:
            card['id'] = str(card['_id'])  # Add 'id' and remove '_id'
            del card['_id']
            flashcards.append(card)

        # print(f'flashcards: {flashcards}')
        data = json.dumps(flashcards)
        print(data)
        # Render the template with the flashcards
        template = request.state.templates.get_template(
            "./flashcards/flashcards_homepage.html")
        return template.render(request=request, data=data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/update')
async def update(data: dict, request: Request):
    word_id_str = data['word_id'].split("'")[3]
    word_id = ObjectId(word_id_str)
    new_known_status = data['known']

    result = await request.app.mongodb.flashcard.update_one(
        {"_id": word_id},
        {"$set": {"known": new_known_status}}
    )

    if result.modified_count > 0:
        return JSONResponse(content={"message": "Progress updated successfully"}, status_code=200)
    else:
        raise HTTPException(
            status_code=500, detail="Failed to update progress")

from flask import Flask, jsonify, request, session
from flask.views import MethodView
from models import Ads, Session
from schema import CreateAds
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


app = Flask('app')


class HttpError(Exception):

    def __init__(self, status_code: int, message: dict | str | list):
        self.status_code = status_code
        self.message = message


def validate(json_data, schema):
    try:
        model = schema(**json_data)
        return model.dict(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, err.errors())


@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    http_response = jsonify({'status': 'error', 'message': er.message})
    http_response.status_code = er.status_code
    return http_response


def get_ads(session: Session, ads_id):
    ads = session.get(Ads, ads_id)
    if ads is None:
        raise HttpError(404, message="Ads doesn't exist!")
    return ads


class AdsView(MethodView):
    def get(self, ads_id):
        with Session() as session:
            ads = get_ads(session,ads_id)
            return jsonify({
                'id': ads.id,
                "title": ads.title,
                "description": ads.description,
                "creation_time": ads.creation_time,
                "owner": ads.owner,
            })


    def post(self):
        json_data = validate(request.json, CreateAds)
        with Session() as session:
            new_ads = Ads(**json_data)
            session.add(new_ads)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(status_code=408, message='Title already exists!')
            return jsonify({'id': new_ads.id})

    def patch(self, user_id):
        pass


    def delete(self, ads_id):
        with Session() as session:
            ads= get_ads(session, ads_id)
            session.delete(ads)
            session.commit()
            return jsonify({"status": "Ads deleted successfully!"})


ads_view = AdsView.as_view('ads')
app.add_url_rule(rule='/ads/', view_func=ads_view, methods=['POST'])
app.add_url_rule(rule='/ads/<int:ads_id>', view_func=ads_view, methods=['GET', 'DELETE'])


if __name__ == '__main__':
    app.run()

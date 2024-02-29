from json import dumps
from app.mailTemplate.service import mailTemplateService
from flask import Blueprint, Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from bson import json_util
from app.mailTemplate import bp

mailTemplateService = mailTemplateService()

@bp.route('/mailTemplate/addMailTemplate', methods=['POST'])
def addMailTemplate():
    try:
        data = request.json
        template = {
            'mailType': data.get('mailType'),
            'subject': data.get('subject'),
            'description': data.get('description'),
        }

        template_id = mailTemplateService.addMailTemplate(template);
        template['_id'] = str(template_id)

        return jsonify({'message': 'Template created successfully.', 'success': True, 'response': template}), 200

    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong', 'success': False}), 500
    #     return jsonify({'ok': True, 'message': 'Question created successfully!', 'response': id}), 200
    # return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400
    
# @bp.route('/mailTemplate/getMailTemplate/<string:type>', methods=['GET'])
def getMailTemplate(type, replacements):
    # replacements = request.json
    template = mailTemplateService.getMailTemplateByType(type)
    if template:
        for replacement in replacements:
            print(replacement)
            template['description'] = template['description'].replace("{{" + replacement['target'] + "}}", replacement['value'])

        template['_id'] = str(template['_id'])
        
        return template
        #json.loads(json_util.dumps(data))
    #     return jsonify({'ok': True, 'message': 'template Fetched!', 'response': template}), 200
    # return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400
    

    


from sphere.bps.meta import get_project, get_project_names
from sphere.lib.utils import get_model


def get_index_content(user):
    """ Контент для главной страницы. Список доступных проектов и документы в них. """
    roles = user.role_set
    res = []

    for project_name in get_project_names():
        if project_name in ('contract', 'contractor'):
            continue

        project = get_project(project_name)

        if not project.roles & roles:
            continue

        document_model = get_model(project.model_name)
        documents = document_model.query.filter(document_model.status != 'archive',
                                                document_model.active == True)

        if 'admin' not in roles:
            documents = documents.filter(document_model.responsible_id == user.id)

        documents_cnt = documents.count()
        if documents_cnt > 0:
            res.append({
                'title': project.title,
                'documents_cnt': documents_cnt,
                'documents': documents[:30],
                'fields': project.document_fields_table,
            })

    return res

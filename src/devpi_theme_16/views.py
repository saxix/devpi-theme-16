from devpi_server.model import UpstreamError
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from devpi_theme_16.main import get_cookie_helper, get_index_url, get_version_url


@view_config(
    route_name="infoview",
    accept="text/html",
    request_method="GET",
    renderer="templates/info.pt")
def infoview(context, request):
    return {}


@view_config(
    route_name="remove",
    accept="text/html",
    request_method=["GET", "POST"],
    renderer="templates/remove.pt")
def remove(context, request):
    if request.method == 'POST':
        if 'cancel' in request.params:
            came_from = get_version_url(context=context,
                                        request=request)
        else:
            came_from = get_index_url(context=context,
                                      request=request)
            stage = context.stage
            name, version = context.project, context.version
            stage.del_versiondata(name, version)
        return HTTPFound(location=came_from)

    project = context.verified_project
    return {"title": project}


@view_config(
    route_name="/{user}",
    accept="text/html",
    request_method="GET",
    renderer="templates/user.pt")
def get_user(context, request):
    user = context.user
    indexes = []
    for index in sorted(user.key.get()['indexes'].keys()):
        stagename = "%s/%s" % (user.name, index)
        stage = context.model.getstage(stagename)
        try:
            packages = len(stage.list_projects_perstage())
        except UpstreamError as e:
            packages = [str(e)]

        indexes.append(dict(
            _ixconfig=stage.ixconfig,
            title=stagename,
            packages=packages,
            index_name=index,
            index_title=stage.ixconfig.get('title', None),
            index_description=stage.ixconfig.get('description', None),
            url=request.stage_url(stagename)))

    user_info = dict(_user=user,
                     name=user.name,
                     # user_name=user.name,
                     title=getattr(user, 'title', None),
                     description=getattr(user, 'description', None),
                     email=getattr(user, 'email', None),
                     indexes=indexes)
    return dict(indexes=indexes,
                user=user,
                user_info=user_info)

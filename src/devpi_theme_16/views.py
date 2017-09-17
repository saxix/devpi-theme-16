from pyramid.view import view_config


@view_config(
    route_name="infoview",
    accept="text/html",
    request_method="GET",
    renderer="templates/info.pt")
def infoview(context, request):
    return {}


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
        indexes.append(dict(
            _ixconfig=stage.ixconfig,
            title=stagename,
            packages=len(stage.list_projects_perstage()),
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

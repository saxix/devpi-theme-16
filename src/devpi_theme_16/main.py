import os
from devpi_lockdown.main import devpiserver_get_credentials
from pyramid.authentication import AuthTktCookieHelper
from pyramid.events import BeforeRender, subscriber

LAST_PACKAGE_FILE = '_last_package'
LAST_VERSION_FILE = '_last_version'


def devpiserver_cmdline_run(xom):
    # this is slightly hacky, because accessing the command line args like that
    # is not part of the official API, but this is just for convenience
    if xom.config.args.theme is None:
        # path = resource_filename('devpi_theme_16', 'theme')
        here = os.path.dirname(__file__)
        path = os.path.realpath(os.path.join(here, 'theme'))
        xom.config.args.theme = path
    else:
        xom.log.error("You are trying to set a theme, "
                      "but devpi-theme-16 is installed.")
        return 1


def devpiserver_pyramid_configure(config, pyramid_config):
    # by using include, the package name doesn't need to be set explicitly
    # for registrations of static views etc
    # see ``includeme`` for actual configuration
    pyramid_config.include('devpi_theme_16.main')


def generated_at(request):
    from devpi_web.views import format_timestamp
    import time

    return format_timestamp(time.time())


def get_index_url(event=None, context=None, request=None):
    request = request or event['request']
    context = context or event['context']
    return request.route_url(
        "/{user}/{index}",
        user=context.user.name,
        index=context.index)


def get_project_url(event=None, context=None, request=None):
    request = request or event['request']
    context = context or event['context']
    return request.route_url(
        "/{user}/{index}/{project}",
        user=context.user.name,
        index=context.index,
        project=context.verified_project)


def get_version_url(event=None, context=None, request=None):
    request = request or event['request']
    context = context or event['context']
    return request.route_url(
        "/{user}/{index}/{project}/{version}",
        user=context.user.name,
        index=context.index,
        project=context.verified_project,
        version=context.version)


def get_cookie_helper(context):
    return AuthTktCookieHelper(context.model.xom.config.secret,
                               cookie_name='auth_tkt',
                               secure=False,
                               include_ip=False,
                               timeout=None,
                               reissue_time=None,
                               max_age=None,
                               http_only=False,
                               path='/',
                               wild_domain=True,
                               hashalg='sha512',
                               parent_domain=False,
                               domain=None)


def get_logged_user(context, request):
    try:
        return devpiserver_get_credentials(request)[0]
    except:
        return ""
    # try:
    #     profile = get_cookie_profile(request)
    #     if profile:
    #         return url_unquote( profile.get_value()).split(':')[0]
    # except AttributeError: # 'HTTPNotFound' object has no attribute 'model'
    #     pass
    # except ValueError:
    #     pass
    # return ""


@subscriber(BeforeRender)
def add_global(event):
    request = event['request']
    context = event['context']
    # event.rendering_val['user'] = getattr(context, 'user')
    identity = get_logged_user(context, request)
    event.rendering_val['identity'] = identity

    if request.matched_route:
        if hasattr(context, 'matchdict'):
            for k, v in context.matchdict.items():
                event.rendering_val[k] = v
        if 'user' in event.rendering_val:
            user = getattr(context, 'user')
            event.rendering_val['user'] = user
        if 'project' in event.rendering_val:
            event.rendering_val['project_url'] = get_project_url(event)
            event.rendering_val['project'] = getattr(context,
                                                     'verified_project')
        if 'version' in event.rendering_val:
            event.rendering_val['version_url'] = get_version_url(event)


def includeme(config):
    config.add_request_method(generated_at, reify=True)
    config.add_route('infoview', '/+info')
    config.add_route('/{user}', '/{user}')
    config.add_route('remove', '/{user}/{index}/{project}/{version}/+remove')
    # config.add_route('web_login', '/+login2')
    # config.add_route('logout', '/+logout')

    config.scan()

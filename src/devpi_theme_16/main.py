from rfc822 import parsedate

from pkg_resources import resource_filename
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from devpi_web.views import format_timetuple

LAST_PACKAGE_FILE = '_last_package'
LAST_VERSION_FILE = '_last_version'


def devpiserver_cmdline_run(xom):
    # this is slightly hacky, because accessing the command line args like that
    # is not part of the official API, but this is just for convenience
    if xom.config.args.theme is None:
        path = resource_filename('devpi_theme_16', 'theme')
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

    # HACK: devpi does not allow override authorization scheme
    # we need to remove the hardcoded IAuthorizationPolicy implementor


# example for a request method
def generated_at(request):
    from devpi_web.views import format_timestamp
    import time

    return format_timestamp(time.time())


def get_project_url(event):
    return event['request'].route_url(
        "/{user}/{index}/{project}",
        user=event['context'].user.name,
        index=event['context'].index,
        project=event['context'].verified_project)


def get_version_url(event):
    return event['request'].route_url(
        "/{user}/{index}/{project}/{version}",
        user=event['context'].user.name,
        index=event['context'].index,
        project=event['context'].verified_project,
        version=event['context'].version)


def get_files_info2(request, linkstore):
    files = []
    filedata = linkstore.get_links(rel='releasefile')

    def ggg(e):
        return e.entry.last_modified

    for link in sorted(filedata, key=ggg):
        last_modified = format_timetuple(parsedate(link.entry.last_modified))
        fileinfo = dict(
            # title=link.basename,
            # url=url,
            # basename=link.basename,
            # hash_spec=entry.hash_spec,
            # dist_type=dist_file_types.get(file_type, ''),
            # py_version=py_version,
            last_modified=last_modified,
            # history=history,
            # size=size
        )
        files.append(fileinfo)
    return files

@subscriber(BeforeRender)
def add_global(event):
    request = event['request']
    context = event['context']
    try:
        if request.matched_route:
            if hasattr(context, 'matchdict'):
                for k, v in context.matchdict.items():
                    event.rendering_val[k] = v
            routename = request.matched_route.name

            if 'version' in event.rendering_val:
                event.rendering_val['version_url'] = get_version_url(event)
            if 'project' in event.rendering_val:
                event.rendering_val['project_url'] = get_project_url(event)

            if '{user}' in routename:
                user = getattr(context, 'user', '')
                event.rendering_val['user'] = user
            if '{index}' in routename:
                index = getattr(context, 'index', '')
                event.rendering_val['index'] = index
            if '{project}' in routename:
                project = getattr(context, 'project', '')
                # event.rendering_val['project'] = project
            # elif routename == "/{user}/{index}/{project}/{version}":
                event.rendering_val['project'] = getattr(context,
                                                         'verified_project', None)
                event.rendering_val['project_url'] = get_project_url(event)

            if routename == "/{user}/{index}/{project}":
                event.rendering_val['owners'] = []
                event.rendering_val['maintainers'] = []
                # event.rendering_val['project_url'] = get_project_url(event)
                try:
                    from devpi_utils.model import RootProjectModel

                    storage = RootProjectModel(context.model.xom)
                    project = storage.get_project(context.project)
                    if project:
                        projectconfig = project.key.get()
                        event.rendering_val['owners'] = projectconfig['owners']
                        event.rendering_val['maintainers'] = projectconfig['maintainers']
                except ImportError:
                    pass
            elif routename == 'docviewroot':
                user = getattr(context, 'user', '')
                event.rendering_val['user'] = user

            elif routename in ['toxresult', 'toxresults']:
                event.rendering_val['user'] = getattr(context, 'user', None)
                event.rendering_val['project_url'] = get_project_url(event)
                event.rendering_val['toxresult'] = 'tox'
            # elif routename == "/{user}/{index}/{project}/{version}":
            #     event.rendering_val['project'] = getattr(context,
            #                                              'verified_project', None)
            #     event.rendering_val['project_url'] = get_project_url(event)
            # elif routename == "/{user}/{index}/{project}":
            #     event.rendering_val['project'] = context.verified_project
            #     event.rendering_val['project_url'] = get_project_url(event)
    except AttributeError:
        pass
    return


def includeme(config):
    config.add_request_method(generated_at, reify=True)
    config.scan()

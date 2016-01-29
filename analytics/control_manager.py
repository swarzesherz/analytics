#coding: utf-8
import datetime

from pyramid.settings import aslist

from dogpile.cache import make_region

from analytics import utils

cache_region = make_region(name='control_manager')

def check_session(wrapped):
    """
        Decorator to check and update session attributes.
    """

    def check(request, *arg, **kwargs):
        collection = request.GET.get('collection', None)
        journal = request.GET.get('journal', None)
        document = request.GET.get('document', None)
        range_start = request.GET.get('range_start', None)
        under_development = request.GET.get('under_development', None)
        range_end = request.GET.get('range_end', None)
        locale = request.GET.get('_LOCALE_', request.locale_name)

        if journal == 'clean' and 'journal' in request.session:
            del(request.session['journal'])
            journal = None
            if 'document' in request.session:
                del(request.session['document'])
                document = None

        if document == 'clean' and 'document' in request.session:
            del(request.session['document'])
            document = None


        session_under_development = request.session.get('under_development', None)
        session_collection = request.session.get('collection', None)
        session_journal = request.session.get('journal', None)
        session_document = request.session.get('document', None)
        session_range_start = request.session.get('range_start', None)
        session_range_end = request.session.get('range_end', None)
        session_locale = request.session.get('_LOCALE_', None)

        if collection and collection != session_collection:
            request.session['collection'] = collection
            if 'journal' in request.session:
                del(request.session['journal'])
        elif not session_collection:
            request.session['collection'] = 'scl'

        if under_development and under_development != session_under_development:
            request.session['under_development'] = under_development

        if journal and journal != session_journal:
            request.session['journal'] = journal

        if document and document != session_document:
            request.session['document'] = document
            request.session['journal'] = document[1:10]

        if range_start and range_start != session_range_start:
            request.session['range_start'] = range_start

        if range_end and range_end != session_range_end:
            request.session['range_end'] = range_end

        if locale and locale != session_locale:
            request.session['_LOCALE_'] = locale

        return wrapped(request, *arg, **kwargs)

    check.__doc__ = wrapped.__doc__

    return check


def base_data_manager(wrapped):
    """
        Decorator to load common data used by all views
    """

    @check_session
    def wrapper(request, *arg, **kwargs):

        @cache_region.cache_on_arguments()
        def get_data_manager(collection, journal, document, range_start, range_end):
            code = document or journal or collection or code
            data = {}

            xylose_doc = request.stats.articlemeta.document(document, collection) if document else None

            if xylose_doc and xylose_doc.publisher_id:
                data['selected_document'] = xylose_doc
                data['selected_document_code'] = document
                journal = document[1:10]

            collections = request.stats.articlemeta.certified_collections()
            journals = request.stats.articlemeta.collections_journals(collection)
            selected_journal = journals.get(journal, None)
            selected_journal_code = journal if journal in journals else None

            today = datetime.datetime.now()
            y3 = today - datetime.timedelta(365*3)
            y2 = today - datetime.timedelta(365*2)
            y1 = today - datetime.timedelta(365*1)

            data.update({
                'collections': collections,
                'selected_code': code,
                'selected_journal': selected_journal,
                'selected_journal_code': selected_journal_code,
                'selected_collection': collections[collection],
                'selected_collection_code': collection,
                'journals': journals,
                'range_start': range_start,
                'range_end': range_end,
                'today': today.isoformat()[0:10],
                'y3': y3.isoformat()[0:10],
                'y2': y2.isoformat()[0:10],
                'y1': y1.isoformat()[0:10]
            })

            return data

        collection_code = request.session.get('collection', None)
        journal_code = request.session.get('journal', None)
        under_development = request.session.get('under_development', '')
        range_end = request.session.get('range_end', datetime.datetime.now().isoformat()[0:10])
        range_start = request.session.get('range_start', (datetime.datetime.now() - datetime.timedelta(365*3)).isoformat()[0:10])
        document_code = utils.REGEX_ARTICLE.match(request.session.get('document', ''))
        if document_code:
            document_code = document_code.string

        data = get_data_manager(collection_code, journal_code, document_code, range_start, range_end)
        data['locale'] = request.session.get('_LOCALE_', request.locale_name)
        data['under_development'] = [i for i in aslist(request.registry.settings.get('under_development', '')) if i != under_development]
        data['google_analytics_code'] = request.registry.settings.get('google_analytics_code', None)
        data['google_analytics_sample_rate'] = request.registry.settings.get('google_analytics_sample_rate', '100')

        setattr(request, 'data_manager', data)

        return wrapped(request, *arg, **kwargs)

    wrapper.__doc__ = wrapped.__doc__

    return wrapper
import logging
from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations

from Acquisition import aq_inner

logger = logging.getLogger('collective.editskinswitcher')
ANNOTATION_KEY = "collective.editskinswitcher"


def get_selected_default_skin(context):
    """Get the selected default skin using annotations."""
    try:
        annotations = IAnnotations(context)
    except TypeError:
        # Not a context that we can handle (seen with
        # Products.CMFUid.UniqueIdAnnotationTool.UniqueIdAnnotation
        # when saving an object).
        return None
    ns = annotations.get(ANNOTATION_KEY, None)
    if ns is not None:
        return ns.get("default-skin", None)


def set_selected_default_skin(context, skin_name=None):
    """Set the specified skin name as the default skin using annotations.

    When the skin_name is None we can remove the annotation if it is there.
    """
    annotations = IAnnotations(aq_inner(context))
    ns = annotations.get(ANNOTATION_KEY, None)
    if ns is None and skin_name is not None:
        # First time here.  Create the annotation.
        ns = annotations[ANNOTATION_KEY] = PersistentMapping()
    elif ns is not None and skin_name is None:
        logger.info("Removed annotation.")
        del annotations[ANNOTATION_KEY]

    if skin_name is not None:
        logger.info("Set the default skin of %s to %s.",
                    context.absolute_url(), skin_name)
        ns["default-skin"] = skin_name

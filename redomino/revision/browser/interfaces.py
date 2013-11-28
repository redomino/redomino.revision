from zope.interface import Interface

class IRedominoRevisionLayer(Interface):
    """ Layer interface """

class IEnableRevisionView(Interface):
    """ Clone revision view """

    def __call__():
        """ Create a new revision folder based on an existing item """

class ICloneRevisionView(Interface):
    """ Clone revision view """

    def __call__():
        """ Create a new revision based on an existing item IRevisionFile """

============
Model Fields
============

Tagulous offers two new model field types:

* :ref:`model_tagfield` - conventional tags using a ``ManyToManyField``
  relationship.
* :ref:`model_singletagfield` - the same UI and functionality as a ``TagField``
  but for a single tag, using a ``ForeignKey`` relationship.

These will automatically create the models for the tags themselves, or you can
provide a custom model to use instead with ``to`` - see
:ref:`custom_tag_models` for more details.

Tagulous lets you get and set string values using these fields, while still
leaving the underlying relationships available. For example, not only can
you assign a queryset or list of tag primary keys to a ``TagField``, but you
can also assign a list of tag names, or a tag string to parse.

Like a ``CharField``, changes made by assigning a value will not be committed
until the model is saved, although you can still make immediate changes by
calling the standard m2m methods ``add``, ``remove`` and ``clear``.

If ``TAGULOUS_ENHANCE_MODELS`` is ``True`` (which it is by default -
see :ref:`settings`), you can also use tag strings and lists of tag names in
``get`` and ``filter``, and model constructors and ``object.create()`` - see
:doc:`tagged_models` for more details.


.. _model_field_arguments:

Model Field Arguments
=====================

The ``SingleTagField`` supports most standard ``ForeignKey`` arguments, except
for ``to_field`` and ``rel_class``.

The ``TagField`` supports most normal ``ManyToManyField`` arguments, except
for ``db_table``, ``through`` and ``symmetrical``. Also note that ``blank`` has
no effect at the database level, it is just used for form validation - as is
the case with a normal ``ManyToManyField``.

The ``related_name`` will default to ``<field>_set``, as is normal for a
``ForeignKey`` or ``ManyToManyField``. If using the same tag table on multiple
fields, you will need to set this to something else to avoid clashes.


.. _field_auto_model:

Auto-generating a tag model
---------------------------

If the :ref:`to argument <argument_to>` is not set, a tag model will be
auto-generated for you. It will be given a class name based on the names of
the tagged model and tag field; for example, the class name of the
auto-generated model for ``MyModel.tags`` would be ``Tagulous_MyModel_tags``.

When auto-generating a model, any :ref:`model option <model_options>` can be
passed as a field argument - see the :ref:`example_auto_tagmodel` example.

If you want to override the default base class, for convenience you can specify
a custom base class for the auto tag model - see the :ref:`argument_to_base`
argument for details.


.. _field_explicit_model:

Specifying a tag model
----------------------

You can specify the tag model for the tag field to use with the
:ref:`to argument <argument_to>`. You cannot specify any tag options.


.. _argument_to:

``to=MyTagModel`` (or first unnamed argument)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manually specify a tag model for this tag field. This can either be a
reference to the tag model class, or string reference to it in the format
``app.model``.

This will normally be a :ref:`custom tag model <custom_tag_models>`, which
must be a subclass of ``tagulous.models.TagModel``.

It can also be a reference to a tag model already auto-generated by another
tag field, eg ``to=MyOtherModel.tags.tag_model``, although you must be
confident that ``MyOtherModel`` will always be defined first.

It can also be a string containing the name of the tag model, eg
``to='MyTagModel'``. However, this is resolved using Django's standard model
name resolution, so you have to reference auto-generated models by their class
name, not via the field - eg ``to='otherapp.Tagulous_MyOtherModel_tags'``.

If the tagged model for this field is also a custom tag model, you can
specify a recursive relationship as normal, using ``'self'``.

If it is a custom tag model, it should have a :ref:`tagmeta` class. Fields
which specify their tag model cannot provide new tag model options; they
will take their options from the model - see :doc:`../tag_options` for more
details.

This argument is optional; if omitted, a tag model will be
:ref:`auto-generated <field_auto_model>` for you.

Default: ``Tagulous_<ModelName>_<FieldName>`` (auto-generated)


.. _argument_to_base:

``to_base=MyTagModelBase``
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can specify a base class to use for an auto-generated tag model, instead of
using ``TagModel``.

This can be useful on complex sites where multiple auto-generated tag models
need to share common custom functionality - for example, tracking and filtering
by user who creates the tags. This argument will allow you to define one base
class and re-use it across your project with less boilerplate than defining
many empty custom tag models.

Default: ``tagulous.models.TagModel``


.. _model_singletagfield:

``tagulous.models.SingleTagField``
==================================

Unbound field
-------------

An unbound ``SingleTagField`` (called on a model class, eg ``MyModel.tag``)
acts in the same way an unbound ``ForeignKey`` field would, but also has:

``tag_model``
    The related tag model

``tag_options``
    A :ref:`TagOptions <tagoptions>` class, containing the options from the tag
    model's :ref:`tagmeta` or passed as arguments when initialising the field.


Bound to an instance
--------------------

A bound ``SingleTagField`` (called on an instance, eg ``instance.tags``) acts
in a similar way to a bound ``ForeignKey``, but with some differences:

Assignment (setter)
    A bound ``SingleTagField`` can be assigned a tag (an instance of the
    tag model) or a tag name.

    If it is passed ``None``, a current tag will be cleared if it is set.

    The instance must be saved afterwards.

    Example::

        person.title = "Mr"
        person.save()

Evaluation (getter)
    The value of a bound ``SingleTagField`` will return an instance of the tag
    model. The tag may not exist in the database yet (its ``pk`` may be
    ``None``).

    Example::

        tag = person.title
        report = "Tag %s used %d times " % (tag.name, tag.count)

The ``tag_model`` and ``tag_options`` attributes are not available on a bound
field. If you only have an instance of the tagged model, you can access them by
finding its class, eg ``type(person).title.tag_model``.



.. _model_tagfield:

``tagulous.models.TagField``
============================

Unbound field
-------------

An unbound ``TagField`` (called on a model class, eg ``MyModel.tags``)
acts in the same way an unbound ``ManyToManyField`` would, but also has:

``tag_model``
    The related tag model

``tag_options``
    A :ref:`TagOptions <tagoptions>` class, containing the options from the tag
    model's :ref:`tagmeta` or passed as arguments when initialising the field.


Bound to an instance
--------------------

A bound ``TagField`` (called on an instance, eg ``instance.tags``) acts
in a similar way to a bound ``ManyToManyField``, but with some differences:

Assignment (setter)
    A bound ``TagField`` can be assigned a tag string or an iterable of tags or
    tag names, eg a list of strings, or a queryset of instances of the tag
    model.

    If it is passed ``None``, any current tags will be cleared.

    The instance must be saved afterwards.

    Example::

        person.skills = 'Judo, "Kung Fu"'
        person.save()

Evaluation (getter)
    A bound ``TagField`` will return a :ref:`tagrelatedmanager` object, which
    has functions to get and set tag values.


.. _tagrelatedmanager:

``tagulous.models.TagRelatedManager``
-------------------------------------

A ``TagRelatedManager`` is a subclass of Django's standard ``RelatedManager``,
so you can do anything you would normally do with a bound ``ManyToManyField``::

    person.skills.get(name='judo')
    tags = person.skills.all()
    person.skills.add(MyTag)
    person.skills.clear()

Because it's a relationship to a :doc:`tag model <tag_models>`, you can also
filter by its fields::

    filtered_tags = person.skills.filter(name__startswith='a')
    popular_tags = person.skills.filter(count__gte=10)

A ``TagRelatedManager`` also provides access to the field's ``tag_model`` and
``tag_options``::

    person.skills.tag_model.objects.all()
    is_lowercase = person.skills.tag_options.force_lowercase

It also provides the following additional methods:


``set_tag_string(tag_string)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sets the tags for this instance, given a tag string.
::

    person.skills.set_tag_string('Judo, "Kung Fu"')
    person.save()


``set_tag_list(tag_list)``
~~~~~~~~~~~~~~~~~~~~~~~~~~
Sets the tags for this instance, given an iterable of tag names or tag
instances.
::

    person.skills.set_tag_list(['Judo', kung_fu_tag])
    person.save()


``get_tag_string()``
~~~~~~~~~~~~~~~~~~~~

Gets the tags as a tag string.
::

    tag_string = person.skills.get_tag_string()
    # tag_string == 'Judo, "Kung Fu"'


``get_tag_list()``
~~~~~~~~~~~~~~~~~~

Returns a list of tag names.
::

    tag_list = person.skills.get_tag_list()
    # tag_list == ['Judo', 'Kung Fu']


``__str__()``, ``__unicode__()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Same as ``get_tag_string``
::

    report = '%s' % person.skills


``__eq__``, ``__ne__``
~~~~~~~~~~~~~~~~~~~~~~
Compare the tags on this instance to a tag string, or an iterable of tags
or tag names. Order does not matter, and case sensitivity is determined by
the options :ref:`option_case_sensitive` and :ref:`option_force_lowercase`.
::

    if (
        first.tags == second.tags
        or first.tags == ['Judo', kung_fu_tag]
        or first.tags != 'foo, bar'
        or first.tags != second.tags.filter(name__istartswith='k')
    ):
        ...


``__contains__``
~~~~~~~~~~~~~~~~
See if the tag (or string of a tag name) is in the tags. Case sensitivity
is determined by the options :ref:`option_case_sensitive` and
:ref:`option_force_lowercase`.
::

    if 'Judo' in person.skills and kung_fu_tag in person.skills:
        candidates.append(person)


``__len__``
~~~~~~~~~~~

.. warning::

    This method is deprecated in Tagulous 0.12, and will be removed in 0.13.

    You should use the `count` manager method instead, eg::

        person.skills = 'judo, "kung fu", karate'
        person.skills.count() == 3


Return the number of tags set for this instance.
::

    person.skills = 'judo, "kung fu", karate'
    len(person.skills) == 3


``reload()``
~~~~~~~~~~~~
Discard any unsaved changes to the tags and load tags from the database
::

    person.skills = 'judo'
    person.save()
    person.skills = 'karate'
    person.skills.reload()
    # person.skills == 'judo'


``save(force=False)``
~~~~~~~~~~~~~~~~~~~~~
Commit any tag changes to the database.

If you are only changing the tags you can call this directly to reduce
database operations.

.. note::
    You do not need to call this if you are saving the instance; the
    manager listens to the instance's save signals and saves any changes
    to tags as part of that process.

In most circumstances you can ignore the ``force`` flag:

* The manager has a ``.changed`` flag which is set to ``False`` whenever
  the internal tag cache is loaded or saved. It is set to ``True`` when the
  tags are changed without being saved.

* If ``force=False`` (default), this method will only update the database
  if the ``.changed`` flag is ``True`` - in other words, the database will
  only be updated if there are changes to the internal cache since last
  load or save.

* If ``force=True``, the ``.changed`` flag will be ignored, and the current
  tag status will be forced upon the database. This can be useful in the
  rare cases where you have multiple references to the same database
  object, and want the tags on this instance to override any changes other
  instances may have made.

For example::

    person = Person.objects.create(name='Adam', skills='judo')
    person.name = 'Bob'
    person.skills = 'karate'
    person.skills.save()
    # person.name == 'Adam'
    # person.skills == 'judo'


``add(tag, tag, ...)``
~~~~~~~~~~~~~~~~~~~~~~
Based on the normal ``RelatedManager.add`` method, but has support for tag
names.

Adds a list of tags or tag names directly to the instance - there is no
need to save afterwards.

.. note::
    This does not parse tag strings - you need to pass separate tags
    as either instances of the tag model, or as separate strings.

Will call ``reload()`` first, so any unsaved changes to tags will be lost.

::

    person.skills.add('Judo', kung_fu_tag)


``remove(tag, tag, ...)``
~~~~~~~~~~~~~~~~~~~~~~~~~
Based on the normal ``RelatedManager.remove`` method, but has support for
tag names.

Removes a list of tags or tag names directly from the instance - there is
no need to save afterwards.

.. note::
    This does not parse tag strings - you need to pass separate tags
    as either instances of the tag model, or as separate strings.

Will call ``reload()`` first, so any unsaved changes to tags will be lost.

::

    person.skills.remove('Judo', kung_fu_tag)


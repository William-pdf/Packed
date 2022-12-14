from django.http import JsonResponse
from django.core.exceptions import FieldDoesNotExist
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import (
    permission_classes,
    api_view,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from .encoders import (
    PackingListItemEncoder,
    PackingListEncoder,
    CategoryEncoder,
    ConditionEncoder,
    ItemEncoder,
)
from .models import (
    PackingListItem,
    PackingList,
    Category,
    Condition,
    Item,
)


def field_does_not_exist_error():
    return JsonResponse(
        {"message": "Invalid field name"},
        status=400,
    )


def model_instance_does_not_exist_message(model_name, pk):
    return JsonResponse(
        {"message": f"'{model_name}' with id number of '{pk}' does not exist"},
        status=400,
    )


def type_error_message(model_name):
    return JsonResponse(
        {"message": f"Failed to create '{model_name}' instance"},
        status=400,
    )


# Category Views -------
@api_view(["GET", "POST"])
def api_categories(request):
    """
    Arguments: the POST method includes a json string containing the data
    needed to create a new catagory.

    Returns: (all json stringified)
    GET: a dictionary with the key of 'categories' containing a queryset
    of all Categories in the database

    POST: a dictionary containing the newly created Category
    """
    if request.method == "GET":
        categories = Category.objects.all().order_by("id")
        return JsonResponse(
            {"categories": categories},
            encoder=CategoryEncoder,
        )
    else:
        try:
            content = json.loads(request.body)
            category = Category.objects.create(**content)
            return JsonResponse(category, encoder=CategoryEncoder, safe=False)
        except TypeError:
            return type_error_message("Category")


@require_http_methods(["GET", "PUT", "DELETE"])
def api_category(request, pk):
    """
    Arguments:
    - pk represents the id number of a category for the PUT and DELETE
    methods
    - for the PUT method, request.body contains json strings of the data
    to be used to update an existing Category

    Returns: (all json stringified)
    GET: a dictionary containing the desired Condition

    POST: a dictionary containing the newly created Condition

    DELETE: a dictionary with the key of 'deleted' and a value of a boolean
    indicating whether the delete was successful or not
    """
    if request.method == "GET":
        try:
            category = Category.objects.get(id=pk)
            return JsonResponse(
                category,
                encoder=CategoryEncoder,
                safe=False,
            )
        except Category.DoesNotExist:
            return model_instance_does_not_exist_message("Category", pk)
    elif request.method == "PUT":
        try:
            content = json.loads(request.body)
            category = Category.objects.filter(id=pk)
            category.update(**content)
            return JsonResponse(
                category,
                encoder=CategoryEncoder,
                safe=False,
            )
        except Category.DoesNotExist:
            return model_instance_does_not_exist_message("Category", pk)
        except FieldDoesNotExist:
            return field_does_not_exist_error()
    else:
        try:
            count, _ = Category.objects.filter(id=pk).delete()
            return JsonResponse({"deleted": count > 0})
        except Category.DoesNotExist:
            return model_instance_does_not_exist_message("Category", pk)


# Item Views ------
def get_user_items(user, included_items):
    """
    This is a helper function used by 'api_conditional_items' that
    removes duplicate suggested items from a list that will be offered
    to the user

    Arguments:
    - user: a User object
    - included_items: a list of Item instances that will be checked
    against for duplicates

    Returns: a list of Item objects
    """
    user_packing_list_items = PackingListItem.objects.filter(owner=user)
    items = []
    for packing_list_item in user_packing_list_items:
        item = Item.objects.get(name=packing_list_item.item_name.name)
        if item not in included_items and item not in items:
            items.append(item)
    return items


@require_http_methods(["GET", "POST"])
def api_items(request):
    """
    Arguments: request.body in the POST method contains a json string
    with the data needed to create a new Item instance

    Returns: (all json stringified)
    GET: a dictionary with the key of 'items' containing a list of all
    Item rows in the database

    POST: a dictionary with a newly created Item row
    """
    if request.method == "GET":
        items = Item.objects.all()
        return JsonResponse({"items": items}, encoder=ItemEncoder)
    else:
        content = json.loads(request.body)
        try:
            if "condition" in content:
                condition = Condition.objects.get(name=content["condition"])
                content["condition"] = condition
            if "category" in content:
                category = Category.objects.get(name=content["category"])
                content["category"] = category
            item = Item.objects.create(**content)
            return JsonResponse(item, encoder=ItemEncoder, safe=False)
        except TypeError:
            return type_error_message("Item")


@api_view(["GET"])
@permission_classes([AllowAny])
def api_conditional_items(request, condition):
    """
    This pivotal function receives a condition from the frontend and handles
    the selection of appropriate items to be returned to the frontend

    Arguments:
    - a string containing the name of an existing condition

    Returns: a json stringified dictionary containing three key-value pairs:
    conditional_items, general_items and user_favorite_items
    """
    if request.method == "GET":
        try:
            conditional_items = []
            if condition != "any":
                condition = Condition.objects.get(name=condition)
                conditional_items = Item.objects.filter(condition=condition)
            any_condition = Condition.objects.get(name="any")
            general_items = Item.objects.filter(condition=any_condition)
            if str(request.user) != "AnonymousUser":
                user_favorite_items = get_user_items(
                    request.user, list(conditional_items) + list(general_items)
                )
            else:
                user_favorite_items = []
            items = {
                "conditional_items": conditional_items,
                "general_items": general_items,
                "user_favorite_items": user_favorite_items,
            }
            return JsonResponse(
                items,
                encoder=ItemEncoder,
                safe=False,
            )
        except Condition.DoesNotExist:
            return JsonResponse(
                {
                    "message": f"'{condition}' may be an invalid condition. Also, make sure you have 'any' condition in database"
                },
                status=400,
            )


@require_http_methods(["GET", "PUT", "DELETE"])
def api_item(request, pk):
    """
    Arguments:
    - pk represents the id number of an Item for the PUT and DELETE
    methods
    - for the PUT method, request.body contains json strings of the data
    to be used to update an existing Item

    Returns: (all json stringified)
    GET: a dictionary containing the desired Item

    POST: a dictionary containing the newly created Item

    DELETE: a dictionary with the key of 'deleted' and a value of a boolean
    indicating whether the delete was successful or not
    """
    if request.method == "GET":
        try:
            item = Item.objects.get(id=pk)
            return JsonResponse(
                item,
                encoder=ItemEncoder,
                safe=False,
            )
        except Item.DoesNotExist:
            return model_instance_does_not_exist_message("Item", pk)
    elif request.method == "DELETE":
        try:
            count, _ = Item.objects.get(id=pk).delete()
            return JsonResponse({"message": count > 0})
        except Item.DoesNotExist:
            return model_instance_does_not_exist_message("Item", pk)
    else:
        try:
            content = json.loads(request.body)
            Item.objects.filter(id=pk).update(**content)
            item = Item.objects.get(id=pk)
            return JsonResponse(item, encoder=ItemEncoder, safe=False)
        except Item.DoesNotExist:
            return model_instance_does_not_exist_message("Item", pk)
        except FieldDoesNotExist:
            return field_does_not_exist_error()


# Condition Views -----
@require_http_methods(["GET", "POST"])
def api_conditions(request):
    """
    Arguments: the POST method includes a json string containing the data
    needed to create a new condition.

    Returns: (all json stringified)
    GET: a dictionary with the key of 'conditions' containing a queryset
    of all Conditions in the database

    POST: a dictionary containing the newly created Condition
    """
    if request.method == "GET":
        all_conditions = Condition.objects.all()
        return JsonResponse(
            {"all conditions": all_conditions},
            encoder=ConditionEncoder,
        )
    else:
        try:
            content = json.loads(request.body)
            condition = Condition.objects.create(**content)
            return JsonResponse(
                condition,
                encoder=ConditionEncoder,
                safe=False,
            )
        except TypeError:
            return type_error_message("Condition")


@require_http_methods(["GET", "DELETE", "PUT"])
def api_condition(request, pk):
    """
    Arguments:
    - pk represents the id number of a condition for the PUT and DELETE
    methods
    - for the PUT method, request.body contains json strings of the data
    to be used to update an existing Condition

    Returns: (all json stringified)
    GET: a dictionary containing the desired Condition

    POST: a dictionary containing the newly created Condition

    DELETE: a dictionary with the key of 'deleted' and a value of a boolean
    indicating whether the delete was successful or not
    """
    if request.method == "GET":
        try:
            condition = Condition.objects.get(id=pk)
            return JsonResponse(
                condition,
                encoder=ConditionEncoder,
                safe=False,
            )
        except Condition.DoesNotExist:
            return model_instance_does_not_exist_message("Condition", pk)
    elif request.method == "DELETE":
        try:
            count, _ = Condition.objects.filter(id=pk).delete()
            return JsonResponse({"deleted": count > 0})
        except Condition.DoesNotExist:
            return model_instance_does_not_exist_message("Condition", pk)
    else:
        try:
            content = json.loads(request.body)
            Condition.objects.filter(id=pk).update(**content)
            condition = Condition.objects.get(id=pk)
            return JsonResponse(condition, encoder=ConditionEncoder, safe=False)
        except Condition.DoesNotExist:
            return model_instance_does_not_exist_message("Condition", pk)
        except FieldDoesNotExist:
            return field_does_not_exist_error()


# PackingList Views -----
def create_packing_list(content):
    """
    This is a helper function for 'api_packing_lists' POST method that
    creates a new PackingList instance

    Arguments: a dictionary containing the content the PackingList will
    be created with

    Returns: the newly created PackingList model instance

    """
    data = {
        "title": content["title"],
        "departure_date": content["departure_date"],
        "return_date": content["return_date"],
        "destination_city": content["destination_city"],
        "destination_country": content["destination_country"],
        "origin_country": content["origin_country"],
        "owner": content["owner"],
    }
    try:
        packing_list = PackingList.objects.create(**data)
        return packing_list
    except KeyError:
        return None


def add_packing_list_item(item, packing_list, owner):
    """
    This is a helper function used by 'api_packing_list_items'
    PUT and POST methods

    It first decides whether the Item passed in already is in the
    database or not. If so, it finds that item and uses it to
    create a new PackingListItme. If not, it creates an Item and
    then creates a PackingListItem with that newly created Item.

    Arguments:
    - a dictionary containing an Item instance
    - a PackingList model instance the PackingListItem will soon
    belong to
    - a User model instance the PackingListItem will soon belong
    to

    Returns:
    an instance of a newly created PackingListItem
    """
    existing_item = Item.objects.filter(name=item["name"])
    if item["suggested"] or len(existing_item) > 0:
        linked_item = Item.objects.get(name=item["name"])
        data = {
            "item_name": linked_item,
            "quantity": int(item["quantity"]),
            "packing_list": packing_list,
            "packed": item.get("packed", False),
            "owner": owner,
        }
    else:
        data = {
            "name": item["name"],
            "suggested": item["suggested"],
            "category": Category.objects.get(name="user"),
            "condition": Condition.objects.get(name="user"),
        }
        linked_item = Item.objects.create(**data)
        data = {
            "item_name": linked_item,
            "quantity": int(item["quantity"]),
            "packing_list": packing_list,
            "packed": item.get("packed", False),
            "owner": owner,
        }
    new_packing_list_item = PackingListItem.objects.create(**data)
    return new_packing_list_item


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def api_packing_lists(request):
    """
    Arguments:
    - for the POST method, the function receives a json string
    containing data to create a new PackingLIst
    - request.user contains the user info to help get the right lists

    Returns: (all json stringified)
    GET: a dictionary containing a list of a user's PackingLists.
    These are formatted in a dictionary with the key of 'packing_lists'
    and the value of a list of dictionaries.

    POST: a dictionary containing the newly created PackingList
    """
    user = request.user
    if request.method == "GET":
        packing_lists = PackingList.objects.filter(owner=user)
        return JsonResponse(
            {"packing_lists": packing_lists},
            encoder=PackingListEncoder,
        )
    else:
        content = json.loads(request.body)
        content["owner"] = user
        packing_list = create_packing_list(content)
        if packing_list:
            return JsonResponse(
                packing_list,
                encoder=PackingListEncoder,
                safe=False,
            )
        else:
            return JsonResponse(
                {"message": "Failed to create packing list"},
                status=400,
            )


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def api_packing_list(request, pk):
    """
    Arugments:
    - an integer representing the ID of a packing list
    - for the PUT method it receives a json string containing updated
    data for one packing list in request.body

    Returns: (all json stringified)
    GET: a dictionary containing the requested PackingList

    PUT: a dictionary containing the updated PackingList

    DELETE: a dictionary with the key of 'deleted' and the value
    of a boolean indicating whether the delete was successful or not
    """
    if request.method == "GET":
        packing_list = PackingList.objects.get(id=pk)
        return JsonResponse(
            packing_list,
            encoder=PackingListEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        try:
            count, _ = PackingList.objects.get(id=pk).delete()
            return JsonResponse(
                {"deleted": count > 0},
            )
        except PackingList.DoesNotExist:
            return model_instance_does_not_exist_message("PackingList", pk)
    else:
        try:
            content = json.loads(request.body)
            packing_list = PackingList.objects.update(**content)
            return JsonResponse(
                packing_list,
                encoder=PackingListEncoder,
                safe=False,
            )
        except PackingList.DoesNotExist:
            return model_instance_does_not_exist_message("PackingList", pk)
        except FieldDoesNotExist:
            return field_does_not_exist_error()


@api_view(["GET", "PUT", "POST"])
@permission_classes([IsAuthenticated])
def api_packing_list_items(request, pk):
    """
    Arguments:
    - an integer representing the ID of a packing list
    - for PUT and POST methods it receives one more many PackingListItems in
    request.body in the format of a json string

    Returns: (all json stringified)
    GET: an object with the key 'items' with a list of dictionaries representing
    all the items in that packing list

    PUT: an object with the key 'items' with a list of dictionaries representing
    all the updated items in that packing list. Note: PackingListObjects are
    ValueObjects and treated as immutable. They are deleted and recreated in this
    mehtod.

    POST: a dictionary with the key 'items' containing a list of dictionaries
    containing the newly created PackingListObjects
    """
    owner = request.user
    if request.method == "GET":
        packing_list = PackingList.objects.get(id=pk)
        items = PackingListItem.objects.filter(packing_list=packing_list)
        return JsonResponse(
            {"items": items},
            encoder=PackingListItemEncoder,
        )

    elif request.method == "PUT":
        content = json.loads(request.body)
        packing_list = PackingList.objects.get(id=pk)
        count, _ = PackingListItem.objects.filter(packing_list=packing_list).delete()
        items = []
        try:
            for item in content["items"]:
                items.append(
                    add_packing_list_item(
                        item=item, packing_list=packing_list, owner=owner
                    )
                )
            return JsonResponse(
                {"items": items},
                encoder=PackingListItemEncoder,
                safe=False,
            )
        except TypeError:
            return type_error_message("Item")

    else:
        content = json.loads(request.body)
        packing_list = PackingList.objects.get(id=pk)
        items = []
        try:
            for item in content["items"]:
                items.append(
                    add_packing_list_item(
                        item=item, packing_list=packing_list, owner=owner
                    )
                )
            return JsonResponse(
                {"items": items},
                encoder=PackingListItemEncoder,
                safe=False,
            )
        except TypeError:
            return type_error_message("Item")

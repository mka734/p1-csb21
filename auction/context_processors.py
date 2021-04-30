from .models import UserData


def extend_user(request):
    if request.user.id is not None:
        user_data = UserData.objects.get(user_id=request.user.id)
        request.user.funds = user_data.funds
        request.user.reserved_funds = user_data.reserved_funds
        request.user.fund_diff = int(
            request.user.funds) - int(request.user.reserved_funds)
        return {
            'user': request.user
        }
    else:
        return {}

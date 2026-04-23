from attendance.models import LeaveRequest


def global_context(request):
    if not request.user.is_authenticated:
        return {}

    pending_leave_count = LeaveRequest.objects.filter(status='pending').count()

    return {
        'pending_leave_count': pending_leave_count,
    }
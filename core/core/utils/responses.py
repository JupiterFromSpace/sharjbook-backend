from rest_framework.response import Response
from rest_framework import status


class SuccessResponse:
    @staticmethod
    def send(
        data=None,
        message="عملیات با موفقیت انجام شد",
        status_code=status.HTTP_200_OK
    ):
        return Response(
            {
                "success": True,
                "message": message,
                "data": data,
            },
            status=status_code
        )


class ErrorResponse:
    @staticmethod
    def send(
        message="درخواست نامعتبر است",
        errors=None,
        status_code=status.HTTP_400_BAD_REQUEST
    ):
        return Response(
            {
                "success": False,
                "message": message,
                "errors": errors,
            },
            status=status_code
        )


class ServerErrorResponse:
    @staticmethod
    def send(
        message="خطای داخلی در پایگاه داده رخ داده است"
    ):
        return Response(
            {
                "success": False,
                "message": message,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

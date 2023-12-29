from rest_framework.response import Response
from rest_framework import status

def retrieve_single_record(model, **kwargs):
    try:
        record = model.objects.get(**kwargs)
        return record    
    except model.DoesNotExist:
        return Response({"error":"Record not found"}, status=status.HTTP_404_NOT_FOUND)
    except model.MultipleObjectsReturned:
        return Response({"error":"Expected to return a single record, but multiple were found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)


def retrieve_multiple_records(model, **kwargs):
    try:
        record_set = model.objects.filter(**kwargs)
        return record_set
    except model.DoesNotExist:
        return Response({"error":"No records found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

from __future__ import division, print_function

import aspose_barcode_cloud
from aspose_barcode_cloud.rest import ApiException
import settings

def get_code(img):
    # Configure OAuth2 access token for authorization: JWT
    configuration = aspose_barcode_cloud.Configuration(
        client_id="d6e1c1d7-1eb2-46d4-8ee3-b4ffd8f2bffe",
        client_secret="9025b92e635bcc289d392c46137fbe41",
    )

    try:
        # create an instance of the API class
        api = aspose_barcode_cloud.BarcodeApi(aspose_barcode_cloud.ApiClient(configuration))

        file = f'{settings.IMG_BAR}{img}.jpg'
        # Recognize barcode
        response = api.post_barcode_recognize_from_url_or_content(image=file,
                                                                preset=aspose_barcode_cloud.PresetType.HIGHPERFORMANCE)
        
        return response.barcodes[0].barcode_value
    except Exception as e:
        print(e)
        return None
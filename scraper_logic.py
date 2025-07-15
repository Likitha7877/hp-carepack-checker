from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from eosl_data import eosl_data
from datetime import datetime, date


printer_mapping = {
      "Y5S43A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "Y5S47A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "Y5S50A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "Y5S54A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "C6N21A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "CC418A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "CE655A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "G3Q37A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "G3Q39A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "G3Q46A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "G3Q47A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "G3Q50A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "T6B51A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "T6B52A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "T6B59A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "T6B60A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "7KW48A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "7KW49A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "7KW63A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "7KW64A": {
        "2 yr add WE": {
            "part": "UG361E"
        },
        "4 yr add WE": {
            "part": "UQ463E"
        },
        "1 yr PW": {}
    },
    "C6N23A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "CB376A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "CE849A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "CZ175A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "G3Q62A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "G3Q66A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "G3Q74A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "G3Q75A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "G3Q68A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "G3Q79A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "G3Q76A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "T6B70A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "T6B71A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "7KW54A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "7KW56A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "F5S29B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "F5S41D": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "F5S42D": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "F5S66A": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "K4U05B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "K7B87D": {
        "2 yr add WE": {
            "part": "UG334E"
        },
        "4 yr add WE": {},
        "1 yr PW": {}
    },
    "V1N02B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "Y5H67D": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "Y5H68D": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "Y5H69D": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "Y5Z03B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "Y5Z04B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "F5S31B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "7WN46D": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "7WN07D": {
        "2 yr add WE": {
            "part": "UG334E"
        },
        "4 yr add WE": {},
        "1 yr PW": {}
    },
    "7WN44D": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "7WQ06B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "7FT02B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "7FR27B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "7FR21B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "7FR53D": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "7FR54D": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "7WQ08B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "7FS80D": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "25R72A": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "M2U76B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "25R69A": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "M2U86B": {
        "2 yr add WE": {
            "part": "UG338E"
        },
        "4 yr add WE": {
            "part": "UZ304E"
        },
        "1 yr PW": {}
    },
    "M2U88B": {
        "2 yr add WE": {
            "part": "UG338E"
        },
        "4 yr add WE": {
            "part": "UZ304E"
        },
        "1 yr PW": {}
    },
    "5SE26B": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "D9L20A": {
        "2 yr add WE": {
            "part": "U6M72E"
        },
        "4 yr add WE": {
            "part": "U6M74E"
        },
        "1 yr PW": {}
    },
    "D9L63A": {
        "2 yr add WE": {
            "part": "UG346E"
        },
        "4 yr add WE": {
            "part": "UZ295E"
        },
        "1 yr PW": {}
    },
    "E3E03A": {
        "2 yr add WE": {
            "part": "UG346E"
        },
        "4 yr add WE": {
            "part": "UZ295E"
        },
        "1 yr PW": {}
    },
    "T0G56A": {
        "2 yr add WE": {
            "part": "U6M72E"
        },
        "4 yr add WE": {
            "part": "U6M74E"
        },
        "1 yr PW": {}
    },
    "3UK97D": {
        "2 yr add WE": {
            "part": "UG350E"
        },
        "4 yr add WE": {
            "part": "UZ299E"
        },
        "1 yr PW": {}
    },
    "3UK98D": {
        "2 yr add WE": {
            "part": "U6M85E"
        },
        "4 yr add WE": {},
        "1 yr PW": {}
    },
    "3UK90D": {
        "2 yr add WE": {
            "part": "UG470E"
        },
        "4 yr add WE": {
            "part": "UZ287E"
        },
        "1 yr PW": {}
    },
    "5LJ20D": {
        "2 yr add WE": {
            "part": "UG349E"
        },
        "4 yr add WE": {
            "part": "UZ298E"
        },
        "1 yr PW": {}
    },
    "4KJ64D": {
        "2 yr add WE": {
            "part": "UG349E"
        },
        "4 yr add WE": {
            "part": "UZ298E"
        },
        "1 yr PW": {}
    },
    "CR768A": {
        "2 yr add WE": {
            "part": "UG348E"
        },
        "4 yr add WE": {
            "part": "UZ297E"
        },
        "1 yr PW": {}
    },
    "G1X85A": {
        "2 yr add WE": {
            "part": "UG348E"
        },
        "4 yr add WE": {
            "part": "UZ297E"
        },
        "1 yr PW": {}
    },
    "G5J38A": {
        "2 yr add WE": {
            "part": "UG348E"
        },
        "4 yr add WE": {
            "part": "UZ297E"
        },
        "1 yr PW": {}
    },
    "CZ993A": {
        "2 yr add WE": {
            "part": "UG348E"
        },
        "4 yr add WE": {
            "part": "UZ297E"
        },
        "1 yr PW": {}
    },
    "N4L17A": {
        "2 yr add WE": {
            "part": "UG348E"
        },
        "4 yr add WE": {
            "part": "UZ297E"
        },
        "1 yr PW": {}
    },
    "Y0S18A": {
        "2 yr add WE": {
            "part": "UG347E"
        },
        "4 yr add WE": {
            "part": "UZ296E"
        },
        "1 yr PW": {}
    },
    "Y0S19A": {
        "2 yr add WE": {
            "part": "UG348E"
        },
        "4 yr add WE": {
            "part": "UZ297E"
        },
        "1 yr PW": {}
    },
    "Z4B55A": {
        "2 yr add WE": {
            "part": "UG337E"
        },
        "4 yr add WE": {
            "part": "UZ303E"
        },
        "1 yr PW": {}
    },
    "Z4B04A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "Z4B53A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "Z6Z11A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "Z6Z13A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "7ZV78A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "Z6Z95A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "Z6Z97A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "1TJ09A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "4SB24A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "4SR29A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "3YW70A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "6UU46A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "6UU47A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "4WF66A": {
        "2 yr add WE": {
            "part": "U35PFE"
        },
        "4 yr add WE": {},
        "1 yr PW": {}
    },
    "4ZB79A": {
        "2 yr add WE": {
            "part": "UB4V5E"
        },
        "4 yr add WE": {
            "part": "UC4Y1E"
        },
        "1 yr PW": {}
    },
    "4ZB80A": {
        "2 yr add WE": {
            "part": "UB4V5E"
        },
        "4 yr add WE": {
            "part": "UC4Y1E"
        },
        "1 yr PW": {}
    },
    "4ZB81A": {
        "2 yr add WE": {
            "part": "UB4V5E"
        },
        "4 yr add WE": {
            "part": "UC4Y1E"
        },
        "1 yr PW": {}
    },
    "4ZB85A": {
        "2 yr add WE": {
            "part": "UB4V5E"
        },
        "4 yr add WE": {
            "part": "UC4Y1E"
        },
        "1 yr PW": {}
    },
    "4ZB86A": {
        "2 yr add WE": {
            "part": "UB4V5E"
        },
        "4 yr add WE": {
            "part": "UC4Y1E"
        },
        "1 yr PW": {}
    },
    "4ZB87A": {
        "2 yr add WE": {
            "part": "UB4V5E"
        },
        "4 yr add WE": {
            "part": "UC4Y1E"
        },
        "1 yr PW": {}
    },
    "4ZB91A": {
        "2 yr add WE": {
            "part": "UB4V5E"
        },
        "4 yr add WE": {
            "part": "UC4Y1E"
        },
        "1 yr PW": {}
    },
    "4ZB92A": {
        "2 yr add WE": {
            "part": "UB4V5E"
        },
        "4 yr add WE": {
            "part": "UC4Y1E"
        },
        "1 yr PW": {}
    },
    "4ZB94A": {
        "2 yr add WE": {
            "part": "UB4W7E"
        },
        "4 yr add WE": {
            "part": "UC4X9E"
        },
        "1 yr PW": {}
    },
    "4ZB95A": {
        "2 yr add WE": {
            "part": "UB4W7E"
        },
        "4 yr add WE": {
            "part": "UC4X9E"
        },
        "1 yr PW": {}
    },
    "4ZB96A": {
        "2 yr add WE": {
            "part": "UB4W7E"
        },
        "4 yr add WE": {
            "part": "UC4X9E"
        },
        "1 yr PW": {}
    },
    "4ZB97A": {
        "2 yr add WE": {
            "part": "UB4W7E"
        },
        "4 yr add WE": {
            "part": "UC4X9E"
        },
        "1 yr PW": {}
    },
    "4QD21A": {
        "2 yr add WE": {
            "part": "UB4X9E"
        },
        "4 yr add WE": {
            "part": "UC4X7E"
        },
        "1 yr PW": {}
    },
    "4RY26A": {
        "2 yr add WE": {
            "part": "UB4X9E"
        },
        "4 yr add WE": {
            "part": "UC4X7E"
        },
        "1 yr PW": {}
    },
    "4RY22A": {
        "2 yr add WE": {
            "part": "UB4Z1E"
        },
        "4 yr add WE": {
            "part": "UC4X5E"
        },
        "1 yr PW": {}
    },
    "4RY23A": {
        "2 yr add WE": {
            "part": "UB4Z1E"
        },
        "4 yr add WE": {
            "part": "UC4X5E"
        },
        "1 yr PW": {}
    },
    "5HG74A": {
        "2 yr add WE": {
            "part": "UB4Z1E"
        },
        "4 yr add WE": {
            "part": "UC4X5E"
        },
        "1 yr PW": {}
    },
    "5HG85A": {
        "2 yr add WE": {
            "part": "UB4X9E"
        },
        "4 yr add WE": {
            "part": "UC4X7E"
        },
        "1 yr PW": {}
    },
    "6GX06A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "6GX04A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "3G635A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "3G636A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "6GW64A": {
        "2 yr add WE": {
            "part": "UG481E"
        },
        "4 yr add WE": {
            "part": "UZ272E"
        },
        "1 yr PW": {}
    },
    "3G658A": {
        "2 yr add WE": {
            "part": "UG481E"
        },
        "4 yr add WE": {
            "part": "UZ272E"
        },
        "1 yr PW": {}
    },
    "CZ174A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    },
    "381U0A": {
        "2 yr add WE": {
            "part": "U04TKE"
        },
        "4 yr add WE": {
            "part": "U04THE"
        },
        "1 yr PW": {}
    },
    "381U2A": {
        "2 yr add WE": {
            "part": "U04TKE"
        },
        "4 yr add WE": {
            "part": "U04THE"
        },
        "1 yr PW": {}
    },
    "381U3A": {
        "2 yr add WE": {
            "part": "U04TKE"
        },
        "4 yr add WE": {
            "part": "U04THE"
        },
        "1 yr PW": {}
    },
    "381U4A": {
        "2 yr add WE": {
            "part": "U04TKE"
        },
        "4 yr add WE": {
            "part": "U04THE"
        },
        "1 yr PW": {}
    },
    "381V6A": {
        "2 yr add WE": {
            "part": "U04SME"
        },
        "4 yr add WE": {
            "part": "U04SKE"
        },
        "1 yr PW": {}
    },
    "3D4L3A": {
        "2 yr add WE": {
            "part": "U57D7E"
        },
        "4 yr add WE": {},
        "1 yr PW": {}
    },
    "1F3W3A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "4A8S4A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "1F3W2A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "4A8R9A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "1F3Y4A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "4A8D9A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "1F3Y2A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "4A8D4A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "6UU48A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "28C12A": {
        "2 yr add WE": {
            "part": "UA5C0E"
        },
        "4 yr add WE": {},
        "1 yr PW": {
            "part": "U9NR3PE"
        }
    },
    "714Z8A": {
        "2 yr add WE": {
            "part": "U62F3E"
        },
        "4 yr add WE": {
            "part": "U62F5E"
        },
        "1 yr PW": {}
    },
    "714Z9A": {
        "2 yr add WE": {
            "part": "U62F3E"
        },
        "4 yr add WE": {
            "part": "U62F5E"
        },
        "1 yr PW": {}
    },
    "715A2A": {
        "2 yr add WE": {
            "part": "U62F3E"
        },
        "4 yr add WE": {
            "part": "U62F5E"
        },
        "1 yr PW": {}
    },
    "715A3A": {
        "2 yr add WE": {
            "part": "U62F3E"
        },
        "4 yr add WE": {
            "part": "U62F5E"
        },
        "1 yr PW": {}
    },
    "715A4A": {
        "2 yr add WE": {
            "part": "U62F3E"
        },
        "4 yr add WE": {
            "part": "U62F5E"
        },
        "1 yr PW": {}
    },
    "715A5A": {
        "2 yr add WE": {
            "part": "U62F3E"
        },
        "4 yr add WE": {
            "part": "U62F5E"
        },
        "1 yr PW": {}
    },
    "53N94C": {
        "2 yr add WE": {
            "part": "UG467E"
        },
        "4 yr add WE": {
            "part": "UZ275E"
        },
        "1 yr PW": {}
    },
    "537P5C": {
        "2 yr add WE": {
            "part": "UG468E"
        },
        "4 yr add WE": {
            "part": "UZ276E"
        },
        "1 yr PW": {}
    },
    "405W2C": {
        "2 yr add WE": {
            "part": "UG349E"
        },
        "4 yr add WE": {
            "part": "UZ277E"
        },
        "1 yr PW": {}
    },
    "404L7C": {
        "2 yr add WE": {
            "part": "U6M85E"
        },
        "4 yr add WE": {},
        "1 yr PW": {}
    },
    "499M6A": {
        "2 yr add WE": {
            "part": "UG482E"
        },
        "4 yr add WE": {
            "part": "UZ260E"
        },
        "1 yr PW": {}
    },
    "499N4A": {
        "2 yr add WE": {
            "part": "UH773E"
        },
        "4 yr add WE": {
            "part": "UZ289E"
        },
        "1 yr PW": {}
    }
}

  

product_page_mapping = {
    "U8LH8E": "u8lh8e-hp-laptop-14-15-series-2-years-additional-warranty-extension",
    "U8LJ4E": "u8lj4e-hp-laptop-14-15-series-2-years-additional-warranty-extension-adp",
    "U8LH7PE": "u8lh7pe-hp-14-15-series-1-year-post-warranty",
    "U8LH9E": "u8lh9e-hp-laptop-14-15-series-factory-warranty-add-on-accidental-damage-protection",
    "UB5R2E": "ub5r2e-hp-14-15-series-2-years-additional-warranty-with-one-time-battery-replacement",
    "U9WX1E": "u9wx1e-hp-3-year-adp",
    "U8LH3E": "u8lh3e-hp14-15-2-year-warranty-extension",
    "UN008E": "un008e-hp-laptop-14-15-series-1-year-additional-warranty-extension-with-accidental-damage-protection",
    "UB5R2E-U9WX1E": "ub5r2e-u9wx1e-hp-14-15-series-2-years-additional-warranty-with-one-time-battery-replacement-and-adp",
    "U0H90E": "u0h90e-hp-pavilion-2-years-additional-warranty-extension",
    "U0H96E": "u0h96e-hp-pavilion-factory-warranty-add-on-accidental-damage-protection",
    "UN009E": "un009e-hp-pavilion-1-year-warranty-extension-adp",
    "U6WD1E": "u6wd1e-hp-pavilion-2-year-warranty-with-accidental-damage-protection-adp",
    "U0H93PE": "u0h93pe-hp-pavilion-1-year-post-warranty",
    "UN006E": "un006e-hp-pavilion-1-year-additional-warranty-extension",
    "UB5R3E": "ub5r3e-hp-pavilion-2-years-additional-warranty-with-one-time-battery-replacement",
    "U6WD2E": "u6wd2e-hp-envy-omen-2-years-additional-warranty-extension-with-accidental-damage-protection-adp",
    "UN010E": "un010e-hp-envy-omen-1-year-additional-warranty-extension-with-accidental-damage-protection-adp",
    "U0H91E": "u0h91e-hp-envy-omen-2-years-additional-warranty-extension",
    "U6WC9E": "u6wc9e-hp-envy-omen-factory-warranty-add-on-with-accidental-damage-protection",
    "UB5R4E": "ub5r4e-hp-envy-omen-2-years-additional-warranty-with-one-time-battery-replacement",
    "UN082PE": "un082pe-hp-envy-omen-1-year-post-warranty",
    "UN007E": "un007e-hp-envy-omen-1-year-additional-warranty-extension",
    "UB5R4E-U9WX1E": "ub5r4e-u9wx1e-hp-envy-omen-2-years-additional-warranty-with-one-time-battery-replacement-and-adp",
    "U0H92E": "u0h92e-hp-spectre-2-years-additional-warranty-extension",
    "U6WD3E": "u6wd3e-hp-spectre-2-years-additional-warranty-extension-with-accidental-damage-protection",
    "UN011E": "un011e-hp-spectre-1-year-additional-warranty-extension-with-accidental-damage-protection",
    "UB5R5E": "ub5r5e-hp-spectre-2-years-additional-warranty-extension-with-one-time-battery-replacement",
    "U0H94PE": "u0h94pe-hp-spectre-1-year-post-warranty-extension",
    "UB5R4E-U9WX1E-1": "ub5r4e-u9wx1e-1-hp-spectre-2-years-additional-warranty-with-one-time-battery-replacement-and-adp",
    "UM952E": "um952e-hp-spectre-1-year-additional-warranty-extension",
    "U6WD0E": "u6wd0e-hp-spectre-factory-warranty-add-on-with-accidental-damage-protection",
    "U02BVE": "u02bve-hp-zbook-g7-g8-g9-factory-warranty-add-on-3-years",
    "U02BSE": "u02bse-hp-z-book-2-years-additional-warranty-extension",
    "U10KHE": "u10khe-hp-z-book-2-years-additional-warranty-extension-adp",
    "U9EE8E": "u9ee8e-hp-200-300-series-4-years-additional-warranty-extension",
    "U9BA7E": "u9ba7e-hp-200-300-series-2-years-additional-warranty-extension",
    "U9BA9E": "u9ba9e-hp-200-300-series-2-years-additional-warranty-extension-with-accidental-damage-protection",
    "U9BA3E": "u9ba3e-hp-200-300-series-1-year-additional-warranty-extension",
    "UB5U0E": "ub5u0e-hp-200-300-series-4-years-additional-warranty-extension-with-accidental-damage-protection-2-claims",
    "U9BB1PE": "u9bb1pe-hp-200-300-series-1-year-post-warranty",
    "U22N8E":"u22n8e-hp-200-300-series-2-years-additional-warranty-extension-on-3-year-care-pack",
    "UK703E": "uk703e-hp-probook-400-laptop-2-years-additional-warranty-extension-1-year-factory-warranty",
    "UK744E": "uk744e-hp-probook-400-laptop-2-years-additional-warranty-extension-on-1-year-base-warranty",
    "UK726E": "uk726e-hp-probook-400-laptop-2-years-additional-warranty-extension-with-accidental-damage-protection-on-1-year-base-warranty",
    "UK718E": "uk718e-hp-probook-400-laptop-4-years-additional-warranty-extension",
    "UK749E": "uk749e-hp-probook-400-laptop-factory-warranty-add-on-accidental-damage-protection",
    "UB8B3E": "ub8b3e-hp-probook-400-laptop-4-years-additional-warranty-extension-with-accidental-damage-protection",
    "UK738PE": "uk738pe-hp-probook-400-laptop-1-year-post-warranty-carepack",
    "U86DXE": "u86dxe-hp-probook-g11-4-years-additional-warranty-extension-1-year-base-warranty/",
    "UB8B6E": "ub8b6e-hp-probook-4xx-2-years-additional-warranty-with-accidental-damage-protection-3-year-base-warranty",
    "UB0E2E": "ub0e2e-hp-elitebook-10xx-2-years-additional-warranty-3-year-base-warranty",
    "UB0E6E": "ub0e6e-hp-elitebook-10xx-2-years-additional-warranty-with-accidental-damage-protection-3-year-base-warranty",
    "UC279E": "uc279ehp-elitebook-fw-adp-3yrs",
    "U4391E": "u4391e-hp-elitebook-2-years-additional-warranty-extension",
    "U7876E": "u7876e-hp-elitebook-7xx-8xx-4-years-additional-warranty-1-year-base-warranty",
    "UC282E": "uc282e-hp-elitebook-fw-adp-1yrs",
    "U7861E": "u7861e-hp-elitebook-2-years-additional-warranty-extension-3-year-base-warranty",
    "UB5T7E": "ub5t7e-hp-elitebook-2-years-additional-warranty-extension-with-accidental-damage-protection-3-year-base-warranty",
    "U5864PE": "u5864pe-hp-all-in-one-business-pc-1-year-post-warranty",
    "U6578E": "u6578e-hp-all-in-one-business-pc-2-years-additional-warranty-extension",
    "U0A84E": "u0a84e-hp-all-in-one-business-pc-factory-warranty-adp",
    "U7899E": "u7899e-hp-all-in-one-business-pc-2-years-additional-warranty-extension-3-year-base-warranty",
    "UF361E": "uf361e-hp-all-in-one-business-pc-3-years-additional-warranty-extension-with-defective-media-retention",
    "U7897E": "u7897e-hp-all-in-one-business-pc-1-year-additional-warranty-extension",
    "U0A85E": "u0a85e-hp-all-in-one-business-pc-1-year-additional-warranty-extension-adp/",
    "U11BVE": "u11bve-hp-all-in-one-business-pc-1-year-additional-warranty-extension-with-defective-media-retention",
    "UF236E": "uf236ehp-all-in-one-business-pc-2-years-additional-warranty-extension-with-accidental-damage-protection-3-year-base-warranty",
    "U0A83E": "u0a83e-hp-all-in-one-business-pc-2-years-additional-warranty-extension-with-accidental-damage-protection",
    "UF360E": "uf360e-hp-all-in-one-business-pc-2-years-additional-warranty-extension-with-defective-media-retention",
    "U7923E": "u7923e-hp-all-in-one-business-pc-3-years-additional-warranty-extension",
    "U7925E": "u7925e-hp-all-in-one-business-pc-4-years-additional-warranty-extension",
    "UJ217E" :"uj217e-hp-desktop-a-i-o-2-years-additional-warranty",
    "U4813PE" :"u4813pe-hp-desktop-a-i-o-1-year-post-warranty",
    "U4813PE" : "u4813pe-hp-desktop-a-i-o-1-year-post-warranty",
    "UA055E" : "ua055e-hp-envy-pavilion-victus-by-hp-omen-by-hp-pro-desktop-2-years-additional-warranty",
    "UA055E": "ua055e-hp-envy-pavilion-victus-by-hp-omen-by-hp-pro-desktop-2-years-additional-warranty",
    "UN062PE": "un062pe-hp-envy-omen-desktop-all-in-one-1-year-post-warranty",
    "U11BWE": "u11bwe-hp-all-in-one-business-pc-2-years-additional-warranty-extension-with-defective-media-retention-3-year-base-warranty/",
    "U11BTE": "u11bte-hp-desktop-3-year-defective-media-retention-on-factory-warranty/",
    "U4813PE": "u4813pe-hp-desktop-a-i-o-1-year-post-warranty",
    "UA055E": "ua055e-hp-envy-pavilion-victus-by-hp-omen-by-hp-pro-desktop-2-years-additional-warranty",
    "UA055E":"ua055e-hp-envy-pavilion-victus-by-hp-omen-by-hp-pro-desktop-2-years-additional-warranty",
    "UN062PE" : "un062pe-hp-envy-omen-desktop-all-in-one-1-year-post-warranty",
    "U4925PE" :"u4925pe-tft-monitor-2-year-additional-warranty-extension-copy",
    "U7935E" : "u7935e-21-tft-monitor-2-year-additional-warranty-extension",
    "U1G24PE" : "u1g24pe-hp-workstation-1-year-post-warranty",
    "U7942E" : "u7942e-workstation-600-800-series-1-year-additional-warranty-extension",
    "U7944E" : "u7944e-workstation-600-800-series-2-year-additional-warranty-extension",
    "U1G39E" : "u1g39e-hp-workstation-400-series-2-year-additional-warranty-extension",
    "U1G37E" : "u1g37e-workstation-400-series-1-year-additional-warranty-extension",
    "U1G57E" : "u1g57e-workstation-400-series-2-year-additional-warranty-extension-with-defective-media-retention",
    "U1G24PE": "u1g24pe-hp-workstation-1-year-post-warranty",
    "UA5C0E": "ua5c0e-hp-smart-tank-aio-2-years-additional-warranty",
    "U35PFE": "u35pfe-hp-smart-tank-790-aio-printer-2-years-additional-warranty",
    "U9NR3PE":"u9nr3pe-hp-smart-tank-aio-1-year-post-warranty",
    "U57D7E": "u57d7e-hp-smart-tank-210-aio-2-years-additional-warranty",
    "UG337E": "ug337e-hp-deskjet-2-years-additional-warranty",
    "UZ303E": "uz303e-hp-deskjet-2-years-additional-warranty-2",
    "UB4V5E": "ub4v5e-hp-laser-10x-and-13x-mfp-2-years-additional-warranty",
    "UC4Y1E": "uc4y1e-hp-laser-10x-and-13x-mfp-4-years-additional-warranty",
    "U62F3E": "hp-laser-u62f3e",
    "U62F5E": "hp-laser-u62f5e",
    "UG337E": "ug337e-hp-deskjet-2-years-additional-warranty",
    "UG338E": "ug338e-hp-deskjet-ia-50xx-aio-printer-2-years-additional-warranty",
    "UZ303E": "uz303e-hp-deskjet-2-years-additional-warranty-2",
    "UZ304E": "uz304e-hp-deskjet-ia-50xx-aio-printer-4-years-additional-warranty",
    "UG334E": "ug334e-hp-deskjet-1112-1212-2-years-additional-warranty",
    "UG348E" : "ug348e-hp-officejet-printers-2-years-additional-warranty-2",
    "UZ297E" : "uz297e-hp-officejet-printers-4-years-additional-warranty-2",
    "UB4W7E": "ub4w7e-hp-color-laser-15x-and-17x-mfp-2-years-additional-warranty",
    "UC4X9E": "uc4x9e-hp-color-laser-15x-and-17x-mfp-4-years-additional-warranty",
    "U5AD9E": "u5ad9e-hp-laserjet-mfp-4-years-additional-warranty-with-defective-media-retention",
    "UH773E": "uh773e-hp-consumer-laserjet-2-years-additional-warranty",
    "UZ289E": "uz289e-hp-consumer-laserjet-4-years-additional-warranty",
    "UG361E": "ug361e-hp-laser-jet-pro-printers-2-years-additional-warranty",
    "UQ463E": "uq463e-hp-laserjet-printers-4-years-additional-warranty",
    "UB9S8E": "ub9s8e-hp-color-laserjet-pro-mfp-m479-4-years-additional-warranty",
    "U04TKE": "u04tke-hp-laserjet-tank-mfp-2-years-additional-warranty",
    "UG481E": "ug481e-hp-laserjet-printer-2-years-additional-warranty",
    "UH773E": "uh773e-hp-consumer-laserjet-2-years-additional-warranty",
    "UZ289E": "uz289e-hp-consumer-laserjet-4-years-additional-warranty",
    "UZ272E": "uz272e-hp-laserjet-printer-4-years-additional-warranty",
    "U04THE": "u04the-hp-laserjet-tank-mfp-4-years-additional-warranty",
    "UG361E": "ug361e-hp-laser-jet-pro-printers-2-years-additional-warranty",
    "U04SME": "u04sme-hp-laserjet-tank-printers-2-years-additional-warranty",
    "UQ463E": "uq463e-hp-laserjet-printers-4-years-additional-warranty",
    "U04SKE": "u04ske-hp-laserjet-tank-1020w-4-years-additional-warranty",
    "UG481E": "ug481e-hp-laserjet-printer-2-years-additional-warranty",
    "UH773E": "uh773e-hp-consumer-laserjet-2-years-additional-warranty",
    "UZ289E": "uz289e-hp-consumer-laserjet-4-years-additional-warranty",
    "UZ272E": "uz272e-hp-laserjet-printer-4-years-additional-warranty",
    "UG361E": "ug361e-hp-laser-jet-pro-printers-2-years-additional-warranty",
    "UQ463E": "uq463e-hp-laserjet-printers-4-years-additional-warranty",
    "U8TM2E": "u8tm2e-hp-laserjet-m402-2-years-additional-warranty",
    "U8TQ9E": "u8tq9e-hp-laserjet-m42x-multi-function-2-years-additional-warranty",
    "U5AD9E": "u5ad9e-hp-laserjet-mfp-4-years-additional-warranty-with-defective-media-retention",
    "UH773E": "uh773e-hp-consumer-laserjet-2-years-additional-warranty",
    "UZ289E": "uz289e-hp-consumer-laserjet-4-years-additional-warranty",
    "UG361E": "ug361e-hp-laser-jet-pro-printers-2-years-additional-warranty",
    "UQ463E": "uq463e-hp-laserjet-printers-4-years-additional-warranty",
    "UC4X7E": "uc4x7e-hp-neverstop-laser-mfp-1200nw-2-years-additional-warranty",
    "UB4X9E": "ub4x9e-hp-neverstop-laser-mfp-1200-nw-2-years-additional-warranty",
    "UB4Z1E": "ub4z1e-hp-neverstop-laser-1xxx-2-years-additional-warranty",
    "UC4X5E": "uc4x5e-hp-neverstop-laser-1xxx-4-years-additional-warranty",
    "UZ277E": "uz277e-hp-officejet-pro-8120-aio-4-year-additional-warranty",
    "UG346E": "ug346e-hp-officejet-printers-2-years-additional-warranty",
    "UG347E": "ug347e-hp-oj-pro-7720-2-years-additional-warranty",
    "U6M74E": "u6m74e-hp-officejet-pro-high-4-years-additional-warranty",
    "UZ299E": "uz299e-hp-oj-pro-9010-4-years-additional-warranty",
    "UZ287E": "uz287e-hp-officejet-pro-9016-aio-printer-4-years-additional-warranty",
    "U6M72E": "u6m72e-hp-officejet-pro-high-2-years-additional-warranty",
    "UZ298E": "uz298e-hp-oj-pro-802x-812x-4-years-additional-warranty",
    "UZ297E": "uz297e-hp-officejet-printers-4-years-additional-warranty-2",
    "UG350E": "ug350e-hp-oj-pro-9010-2-years-additional-warranty",
    "UZ296E": "uz296e-hp-officejet-pro-7720-wide-format-4-years-additional-warranty",
    "U6M85E": "u6m85e-hp-officejet-pro-printer-2-years-additional-warranty",
    "UG467E": "ug467e-hp-officejet-pro-9720-wf-aio-2-years-additional-warranty",
    "UG470E": "ug470e-hp-officejet-pro-9016-aio-printer-2-years-additional-warranty",
    "UG468E": "ug468e-hp-officejet-pro-9730-wf-aio-2-years-additional-warranty/",
    "UG349E": "ug349e-hp-oj-pro-802x-812x-2-years-additional-warranty",
    "UZ275E": "uz275e-hp-officejet-pro-9720-wf-aio-4-years-additional-warranty",
    "UG348E": "ug348e-hp-officejet-printers-2-years-additional-warranty-2",
    "UZ276E": "uz276e-hp-officejet-pro-9730-wf-aio-5-years-additional-warranty",
    # Add other parts mapping here...


   
}

product_title_mapping = {
   "U8LH8E": {
    "title": "HP Laptop 14/15 Series 2 Years Additional Warranty Extension",
    "price": "6000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/09/14-15s-2HW-1-2.webp",
    "tag"  : "Essentials",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U8LJ4E": {
    "title": "HP Laptop 14/15 Series 2 Years Additional Warranty Extension with Accidental Damage Protection",
    "price": "11500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/09/14-15s-2HWADP.png",
    "tag"  :"Smart Pick",
    "coverage":"in-warranty",
    "duration":"3 year"
    
  },
  "U8LH3E": {
    "title": "HP Laptop 14/15 Series 1 year Additional Warranty Extension",
    "price": "4000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-1HW-3.webp",
    "coverage": "in-warranty",
    "duration":"2 year"
    
  },
  "UN008E": {
    "title": "HP Laptop 14/15 Series 1 Year Additional Warranty Extension with Accidental Damage Protection",
    "price": "7500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-1HWADP.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U8LH9E": {
    "title": "HP Laptop 14/15 Series Factory Warranty add-on Accidental Damage Protection",
    "price": "4500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-ADP.webp",
    "coverage":"in-warranty",
    "duration":"1 year"
  },
  "UB5R2E": {
    "title": "HP 14/15 Series 2 Years Additional Warranty with One-Time Battery Replacement",
    "price": "10000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-2HWBATT.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U8LH7PE": {
    "title": "HP 14/15 Series 1 year Post Warranty",
    "price": "5500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-PW.webp",
    "coverage":"post-warranty",
    "duration":"1 year"
  },
  "U0H90E": {
    "title": "HP Pavilion/Victus by HP 2 Years Additional Warranty Extension",
    "price": "9000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-2HW.webp",
    "tag":"Essentials",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U6WD1E": {
    "title": "HP Pavilion/Victus by HP 2-Year Warranty with Accidental Damage Protection (ADP)",
    "price": "15500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-2HWADP.webp",
    "tag":"Smart Pick",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "UN006E": {
    "title": "HP Pavilion/Victus by HP 1-Year Additional Warranty Extension",
    "price": "5500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-1HW.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "UN009E": {
    "title": "HP Pavilion/Victus by HP 1-Year Warranty Extension with Accidental Damage Protection (ADP)",
    "price": "9500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-1HWADP.webp",
    "tag":"Customer favourite",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U0H96E": {
    "title": "HP Pavilion/Victus by HP Factory Warranty Add-On Accidental Damage Protection",
    "price": "4500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-ADP.webp",
    "coverage":"in-warranty",
    "duration":"1 year"
  },
  "UB5R3E": {
    "title": "HP Pavilion/Victus by HP 2 Years Additional Warranty with One-Time Battery Replacement",
    "price": "12500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-2HWBATT.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U0H93PE": {
    "title": "HP Pavilion/Victus by HP 1 year Post Warranty",
    "price": "8200",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-PW.webp",
    "coverage":"post-warranty",
    "duration":"1 year"
    
  },
   "U0H91E": {
    "title": "HP Envy/Omen 2 Years Additional Warranty Extension",
    "price": "15500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-2HW.webp",
    "tag":"Essentials",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
    "UB5R3E-U9WX1E": {
    "title": "HP Pavilion/Victus by HP 2 Years Additional Warranty with One-Time Battery Replacement and ADP",
    "price": "20999",
    "image": "https://arminfoserve.com/wp-content/uploads/2025/04/Pavilion-2ADPBATT.png",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  
  "UN007E": {
    "title": "HP Envy/Omen 1 Year Additional Warranty Extension",
    "price": "8500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-1HW.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U6WD2E": {
    "title": "HP Envy/Omen 2 Years Additional Warranty Extension with Accidental Damage Protection",
    "price": "24500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-2HWADP.webp",
    "coverage":"in-warranty",
    "duration":"3 year",
    "tag":"Smart Pick"
  },
  "UN010E": {
    "title": "HP Envy/Omen 1-year Additional Warranty Extension with Accidental Damage Protection",
    "price": "12500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-1HWADP.webp",
    "coverage":"in-warranty",
    "duration":"2 year",
    "tag":"Customer Favourite"
  },
  "U6WC9E": {
    "title": "HP Envy/Omen Factory Warranty Add-On with Accidental Damage Protection",
    "price": "6500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-ADP.webp",
    "coverage":"in-warranty",
    "duration":"1 year"
  },
  "UB5R4E": {
    "title": "HP Envy/Omen 2 Years Additional Warranty with One-Time Battery Replacement",
    "price": "23000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-2HWBATT.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "UN082PE": {
    "title": "HP Envy/Omen 1 year Post Warranty",
    "price": "14000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-PW.webp",
    "coverage":"post-warranty",
    "duration":"1 year"
  },
  "U9WX1E": {
    "title": "Accidental Damage Protection Add on for 3 years Extended Warranty",
    "price": "0",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/09/14-15s-2HW-1-2.webp",
    "coverage": "in-warranty",
    "duration":"3 year"
  },
   "U0H92E": {
    "title": "HP Spectre 2 Years Additional Warranty Extension",
    "price": "18250",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-2HW.webp",
    "tag":"Essentials",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U6WD3E": {
    "title": "HP Spectre 2 Years Additional Warranty Extension with Accidental Damage Protection",
    "price": "26000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Spectre-2HWADP.webp",
    "tag":"Smart Pick",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "UM952E": {
    "title": "HP Spectre 1 year Additional Warranty Extension",
    "price": "12000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-1HW.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "UN011E": {
    "title": "HP Spectre 1 year Additional Warranty Extension with Accidental Damage Protection",
    "price": "17100",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Spectre-1HWADP.webp",
    "tag":"Customer favourite",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U6WD0E": {
    "title": "HP Spectre Factory Warranty Add-On with Accidental Damage Protection",
    "price": "8500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Spectre-ADP.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "UB5R5E": {
    "title": "HP Spectre 2 Years Additional Warranty Extension with One time Battery Replacement",
    "price": "27500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Spectre-2HWBATT.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U0H94PE": {
    "title": "HP Spectre 1 year Post Warranty Extension",
    "price": "24500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Spectre-PW.webp",
    "coverage":"post-warranty",
    "duration":"1 year"
  },
   "UB5R4E-U9WX1E-1": {
    "title": "HP Spectre 2 Years Additional Warranty with One-Time Battery Replacement and ADP",
    "price": "32999",
    "image": "https://arminfoserve.com/wp-content/uploads/2025/04/Pavilion-2ADPBATT.png",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U9BA7E": {
    "title": "HP 200/300 Series 2 years Additional Warranty Extension",
    "price": "5556",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/200-2HW-1.webp",
    "tag":"Essentials",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U9BA3E": {
    "title": "HP 200/300 Series 1 Year Additional Warranty Extension",
    "price": "3000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/200-1HW.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U9BA9E": {
    "title": "HP 200/300 Series 2 years Additional Warranty Extension with Accidental Damage Protection",
    "price": "10556",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/200-2HWADP.webp",
    "tag":"Customer favourite",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U9EE8E": {
    "title": "HP 200/300 Series 4 years Additional Warranty Extension",
    "price": "10556",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/200-4HW.webp",
    "duration":"5 year",
    "coverage":"in-warranty"

  },
   "U9EE8E": {
    "title": "HP 200/300 Series 2 years Additional Warranty Extension on 3 year Care Pack",
    "price": "10500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/200-2HW-1.webp",
    "duration":"5 year",
    "coverage":"in-warranty"

  },
  "UB5U0E": {
    "title": "HP 200/300 Series 4 years Additional Warranty Extension with Accidental Damage Protection",
    "price": "15000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/200-4HWADP.webp",
    "tag":"Smart Pick",
    "duration":"5 year",
    "coverage":"in-warranty"
  },
  "U9BB1PE": {
    "title": "HP 200/300 Series 1 year Post Warranty",
    "price": "5556",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/200-PW.webp",
    "coverage":"post-warranty",
    "duration":"1 year"
  },
  "UK744E": {
    "title": "HP ProBook 400 laptop 2 years Additional Warranty Extension (3 year factory warranty)",
    "price": "10556",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/ProB-2HW-1.webp",
    "coverage":"in-warranty",
    "duration":"5 year"
  },
  "UK726E": {
    "title": "HP ProBook 4XX 2 years Additional Warranty Extension with Accidental Damage Protection (1 Year Base Warranty)",
    "price": "10556",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/ProB-2HWADP.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "UK718E": {
    "title": "HP ProBook 400 laptop 4 years Additional Warranty Extension (1 year Base Warranty)",
    "price": "14000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/ProB-4HW.webp",
    "coverage":"in-warranty",
    "duration":"5 year"
  },
  "U86DXE":{
    "title": "HP ProBook G11 4 years Additional Warranty Extension (1 year Base Warranty)",
    "price": "14000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/ProB-4HW.webp",
    "coverage":"in-warranty",
    "duration":"5 year"
      },
  "UK749E": {
    "title": "HP ProBook 400 3 years Factory Warranty Accidental Damage Protection",
    "price": "8111",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/ProB-ADP.webp",
    "coverage":"in-warranty",
    "duration":"5 year"
  },
  "UB8B3E": {
    "title": "HP ProBook 400 laptop 4 years Additional Warranty Extension with Accidental Damage Protection (1 Year Base Warranty)",
    "price": "18778",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/ProB-4HWADP.webp",
    "coverage":"in-warranty",
    "duration":"5 year"
  },
  "UK738PE": {
    "title": "HP ProBook 400 laptop 1 year Post Warranty Care Pack",
    "price": "8111",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/ProB-PW.webp",
    "coverage":"post-warranty",
    "duration":"1 year"
  },
  "UK703E": {
    "title": "HP ProBook 400 laptop 2 years Additional Warranty Extension (1 year factory warranty)",
    "price": "8111",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/ProB-2HW.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "UB8B6E": {
    "title": "HP ProBook 4XX 2 years Additional Warranty with Accidental Damage Protection (3 Year Base Warranty)",
    "price": "15000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/ProB-2HWADP-1.webp" ,
    "coverage":"in-warranty",
    "duration":"5 year"
  },
  "U86E0E":{
    "title": "HP ProBook G11 laptop 4 years Additional Warranty Extension with Accidental Damage Protection (1 Year Base Warranty)",
    "price": "17000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/ProB-4HWADP.webp" ,
    "coverage":"in-warranty",
    "duration":"5 year"
    },
  "U86DVE":{
    "title": "HP ProBook G11 laptop 2 years Additional Warranty Extension (1 year factory warranty)",
    "price": "8000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/ProB-2HW.webp" ,
    "coverage":"in-warranty",
    "duration":"3 year"
    },
  
  "U7876E": {
    "title": "HP Elitebook 7xx/8xx 4 years additional warranty (1 year base warranty)",
    "price": "32500",
    "image": "https://arminfoserve.com/wp-content/uploads/2025/04/Elite-4HW.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "UC279E":{
    "title": "HP EliteBook 3-year Accidental Damage Protection on Factory Warranty",
    "price": "10,556",
    "image": "https://i0.wp.com/arminfoserve.com/wp-content/uploads/2024/01/Elite-ADP.webp?fit=520%2C400&ssl=1",
    "coverage":"in-warranty",
    
  },
  "UC282E":{
    "title": "HP EliteBook 3 year Accidental Damage Protection on 1 year Factory Warranty",
    "price": "18,778",
    "image": "https://i0.wp.com/arminfoserve.com/wp-content/uploads/2024/01/Elite-ADP-1.webp?fit=520%2C400&ssl=1",
    "coverage":"in-warranty",
    "duration":"3 year"   
  },
  "UB0E2E": {
    "title": "HP EliteBook 10xx 2 years additional warranty (3 year base warranty)",
    "price": "16000",
    "image": "https://arminfoserve.com/wp-content/uploads/2025/04/Elite-4HW.png",
    "coverage":"in-warranty",
    "duration":"5 year"
  },
  "UB0E6E": {
    "title": "HP EliteBook 10xx 2 years additional warranty with Accidental Damage Protection (3 year base warranty)",
    "price": "23000",
    "image": "https://arminfoserve.com/wp-content/uploads/2025/04/Elite-4HW.png",
    "coverage":"in-warranty",
    "duration":"5 year"
  },
  "U7861E": {
    "title": "HP EliteBook 2 Years Additional Warranty Extension (3 Year Base Warranty)",
    "price": "12222",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Elite-2HW-2.webp",
    "coverage":"in-warranty",
    "duration":"5 year"
  },
  "UB5T7E": {
    "title": "HP EliteBook 2 Years Additional Warranty Extension with Accidental Damage Protection (3 Year Base Warranty)",
    "price": "19889",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Elite-2HWADP-2.webp",
    "coverage":"in-warranty",
    "duration":"5 year"
  },
  
  "U4391E": {
    "title": "HP EliteBook 2 Years Additional Warranty Extension (1 Year Base Warranty)",
    "price": "12222",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Elite-2HW-1.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  #desktops
  #hp aio bussines
  "U5864PE": {
    "title": "HP All-in-One Business PC 1 year Post Warranty",
    "price": "5850",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/10/AIO-PW-1.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U6578E": {
    "title": "HP All-in-One Business PC 2 Years Additional Warranty Extension (1 Year Base Warranty)",
    "price": "5600",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/AIO-2HW.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U7899E": {
    "title": "HP All-in-One Business PC 2 Years Additional Warranty Extension (3 Year Base Warranty)",
    "price": "4667",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/07/AIO-2HW-1.webp",
    "coverage":"in-warranty",
    "duration":"5 year"
  },
  "U0A84E": {
    "title": "HP All-in-One Business PC Factory Warranty Add-on Accidental Damage Protection",
    "price": "9445",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/AIO-ADP-1.webp",
    "coverage":"in-warranty",
    "duration":"1 year"
  },
  
  "U7897E": {
    "title": "HP All-in-One Business PC 1 year Additional Warranty Extension",
    "price": "5000",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/AIO-1HW.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U0A85E": {
    "title": "HP All-in-One Business PC 1 year Additional Warranty Extension with Accidental Damage Protection",
    "price": "7250",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/AIO-1HWADP.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U11BVE": {
    "title": "HP All-in-One Business PC 1 year Additional Warranty Extension with Defective Media Retention",
    "price": "6944",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/AIO-1HWDMR.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "UF236E": {
    "title": "HP All-in-One Business PC 2 Years Additional Warranty Extension with Accidental Damage Protection (3 Year Base Warranty)",
    "price": "13900",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/07/AIO-2HWADP-2.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U0A83E": {
    "title": "HP All-in-One Business PC 2 Years Additional Warranty Extension with Accidental Damage Protection (1 Year Base Warranty)",
    "price": "8500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/AIO-2HWADP.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "UF360E": {
    "title": "HP All-in-One Business PC 2 Years Additional Warranty Extension with Defective Media Retention (1 Year Base Warranty)",
    "price": "7800",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/AIO-2HWDMR.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U7923E": {
    "title": "HP All-in-One Business PC 3 Years Additional Warranty Extension",
    "price": "8500",
    "image": "https://i0.wp.com/arminfoserve.com/wp-content/uploads/2023/11/AIO-3HW.webp?fit=520%2C400&ssl=1",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
   "U7925E": {
    "title": "HP All-in-One Business PC 4 Years Additional Warranty Extension",
    "price": "9800",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/AIO-4HW.webp",
    "coverage":"in-warranty",
    "duration":"5 year"
  },
    "UF361E": {
    "title": "HP All-in-One Business PC 3 Years Additional Warranty Extension with Defective Media Retention",
    "price": "10500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/AIO-3HWDMR.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  
  
  
  
   #hp aio desk
  "UJ217E": {
    "title": "HP Desktop/All-In-One 2 Years Additional Warranty",
    "price": "7500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/TFT-2HW.png",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U4813PE": {
    "title": "HP Desktop/All-In-One 1 Year Post Warranty",
    "price": "5000",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/10/AIO-PW-1.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  #pavilion aio/desk,#envy aio/desk
   "U4813PE": {
    "title": "HP Desktop/All-In-One 1 Year Post Warranty",
    "price": "5000",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/10/AIO-PW-1.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
   "UA055E": {
    "title": "HP Envy/Pavilion/Victus by HP/Omen by HP/Pro Desktop 2 Years Additional Warranty",
    "price": "13500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/AIO-2HW.png",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
   
   "UN062PE": {
    "title": "HP Envy/Omen Desktop/All-In-One 1 Year Post Warranty",
    "price": "9850",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/10/AIO-PW-1.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
   #HP Business Desktop
   "U11BWE": {
    "title": "HP Desktop 2 Years Additional Warranty Extension with DMR (3 Year Factory Warranty)",
    "price": "7222",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/07/AIO-2HWDMR-1.webp",
    "coverage":"in-warranty",
    "duration":"5 year"
  },
   "U11BTE": {
    "title": "HP Desktop 3 year Defective Media Retention on Factory Warranty",
    "price": "6556",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/11/AIO-3DMR.png",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
   #TFT Monitor
    "U4925PE": {
    "title": "TFT Monitor 1-year Post Warranty",
    "price": "3500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/TFT-PW.png",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
    "U7935E": {
    "title": "Up to 24in TFT Monitor 2-year Additional Warranty Extension",
    "price": "4500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/TFT-2HW.png",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
    #workstation 6xx-8xx/hp workstation 4xx
    
    "U1G24PE": {
    "title": "HP WorkStation 1 Year Post Warranty",
    "price": "13899",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/07/AIO-PW-2.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
    "U7944E": {
    "title": "WorkStation 600/800 SERIES 2-year Additional Warranty Extension",
    "price": "12500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/WS-2HW-1.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
    "U7942E": {
    "title": "WorkStation 600/800 SERIES 1-year Additional Warranty Extension",
    "price": "8500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/WS-1HW-1.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
    "U1G37E": {
    "title": "WorkStation 400 SERIES 1 year Additional Warranty Extension",
    "price": "7650",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/WS-1HW-1-1.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
   "U1G57E": {
    "title": "WorkStation 400 SERIES 2-year Additional Warranty Extension with Defective Media Retention",
    "price": "11500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/WS-2HWDMR.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },

   "U1G39E": {
    "title": "WorkStation 400 SERIES 2-year Additional Warranty Extension",
    "price": "10000",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/11/WS-2HW-1-1.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
   
   
  
# printers
    "UA5C0E": {
    "title": "HP Smart Tank AiO 2 years Additional Warranty",
    "price": "4000",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Smart-tank-AIO-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "U35PFE": {
    "title": "HP Smart Tank 790 AiO Printer 2 years Additional Warranty",
    "price": "5000",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Smart-tank-AIO-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "U57D7E": {
    "title": "HP Smart Tank 210 AiO 2 years Additional Warranty",
    "price": "5000",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Smart-tank-AIO-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "U9NR3PE": {
    "title": "HP Smart Tank AiO 1 year Post Warranty",
    "price": "3611",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Smart-tank-AIO-1.png",
    "duration": "1 year",
    "coverage":"post-warranty",
  },
  "UG361E": {
    "title": "HP LaserJet Pro Printers 2 years Additional Warranty",
    "price": "4444",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laserjet-pro-MFP-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UH769E": {
    "title": "HP 3-Year Pickup and Return for Consumer LaserJet - Entry Service",
    "price": "5075",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laserjet-pro-MFP-1.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "UG337E": {
    "title": "HP Multi-function Printer 2 years Additional Warranty",
    "price": "5167",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UG062E": {
    "title": "HP DeskJet IA Ultra 4826 AiO Printer 2 years Additional Warranty",
    "price": "4667",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UG334E": {
    "title": "HP Deskjet 1112, 1212 2 years Additional Warranty",
    "price": "4222",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UG338E": {
    "title": "HP DeskJet IA 50XX AiO Printer 2 years Additional Warranty",
    "price": "4444",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "U6M72E": {
    "title": "HP OfficeJet Pro High 2 years Additional Warranty",
    "price": "7222",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UG346E": {
    "title": "HP Officejet Printers 2 years Additional Warranty",
    "price": "4667",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UG350E": {
    "title": "HP OJ Pro 9010 2 years Additional Warranty",
    "price": "6222",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "U6M85E": {
    "title": "HP OfficeJet Pro Printer (Ultra High) 2 years Additional Warranty",
    "price": "8889",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  
  "UG470E": {
    "title": "HP OfficeJet Pro 9016 AiO Printer 2 years Additional Warranty",
    "price": "6556",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UG349E": {
    "title": "HP OJ Pro 802X, 812X 2 years Additional Warranty",
    "price": "5889",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UG348E": {
    "title": "HP Officejet Printers 2 years Additional Warranty",
    "price": "5167",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UG347E": {
    "title": "HP OJ Pro 7720 2 years Additional Warranty",
    "price": "5167",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
 
  "U35PFE": {
    "title": "HP Smart Tank 790 AiO Printer 2 years Additional Warranty",
    "price": "5000",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Smart-tank-AIO-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UB4V5E": {
    "title": "HP Laser 10x and 13x MFP 2 years Additional Warranty",
    "price": "4833",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration":"3 year",
    "coverage":"in-warranty"
  },
  "UB4W7E": {
    "title": "HP Color Laser 15x and 17x MFP 2 years Additional Warranty",
    "price": "7778",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP.webp",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UB4X9E": {
    "title": "HP Neverstop Laser MFP 1200nw 2 years Additional Warranty",
    "price": "6889",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Neverstop-Laser-MFP.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UB4Z1E": {
    "title": "HP Neverstop Laser 1xxx 2 years Additional Warranty",
    "price": "6222",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Neverstop-Laser-MFP.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UH773E": {
    "title": "HP Consumer LaserJet 2 years Additional Warranty",
    "price": "5556",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UZ298E": {
    "title": "HP OJ Pro 802X, 812X 4 years Additional Warranty",
    "price": "7427",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "UZ297E": {
    "title": "HP Officejet Printers 4 years Additional Warranty",
    "price": "7427",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-AIO.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "UZ296E": {
    "title": "HP OfficeJet Pro 7720 Wide Format 4 years Additional Warranty",
    "price": "6670",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "UC4Y1E": {
    "title": "HP Laser 10x and 13x MFP 4 years Additional Warranty",
    "price": "7427",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration":"5 year",
    "coverage":"in-warranty"
  },
  "UC4X9E": {
    "title": "HP Color Laser 15x and 17x MFP 4 years Additional Warranty",
    "price": "11440",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "UC4X7E": {
    "title": "HP Neverstop Laser MFP 1200nw 4 years Additional Warranty",
    "price": "11267",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Neverstop-Laser-MFP.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "UC4X5E": {
    "title": "HP Neverstop Laser 1xxx 4 years Additional Warranty",
    "price": "10176",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Neverstop-Laser-MFP.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "UZ289E": {
    "title": "HP Consumer LaserJet 4 years Additional Warranty",
    "price": "6812",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "UZ272E": {
    "title": "HP LaserJet Printer 4 years Additional Warranty",
    "price": "6822",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laserjet-pro-MFP-1.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "U04THE": {
    "title": "HP LaserJet Tank MFP 4 years Additional Warranty",
    "price": "12567",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP.png",
    "duration":"5 year",
    "coverage":"in-warranty"
  },
  "U04TKE": {
    "title": "HP LaserJet Tank MFP 2 years Additional Warranty",
    "price": "6,667",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP.png",
    "duration":"3 year",
    "coverage":"in-warranty"
  },
  "U04SKE": {
    "title": "HP LASERJET TANK 1020W 4 years Additional Warranty",
    "price": "11307",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/LaserJet.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "U62F5E": {
    "title": "HP Laser 100x and 11xx MFP 4 years Additional Warranty",
    "price": "7427",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "U8TM2E": {
    "title": "HP LaserJet M402 2 years Additional Warranty",
    "price": "8120",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/LaserJet.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "U8TN1E": {
    "title": "HP Color LaserJet M452 2 years Additional Warranty",
    "price": "10199",
    "image":"https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration": "3 year",
    "coverage":"in-warranty"

  },
  "U8TQ9E": {
    "title": "HP LaserJet M42x Multi-Function 2 years Additional Warranty",
    "price": "17369",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP.png",
    "duration": "3 year",
    "coverage":"in-warranty"
      
  },
  "U9JT1E": {
    "title": "HP Installation Service with network configuration for Personal Scanner and Printer (1 unit)",
    "price": "5850",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP.png"
      
  },
  "U6Z65E": {
    "title": "HP 2 years Additional Next Business Day + Defective Media Retention",
    "price": "33125",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP.png",
    "duration": "3 year",
    "coverage":"in-warranty"
     
  },
  "U5AD9E": {
    "title": "HP LaserJet MFP 4 years Additional Warranty with Defective Media Retention",
    "price": "40540",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP.png",
    "duration": "5 year",
    "coverage":"in-warranty"
      
  },
  "UB9R9E": {
    "title": "HP LaserJet Pro MFP M429fdn, M429fdw 4 years Additional Warranty",
    "price": "21599",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
  "UB9R7E": {
    "title": "HP LaserJet Pro MFP M429dw, M329dn, M329dw 2 years Additional Warranty",
    "price": "10200",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UB9S8E": {
    "title": "HP Color LaserJet Pro MFP M479 4 years Additional Warranty",
    "price": "25047",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP-1.webp",
    "duration": "5 year",
    "coverage":"in-warranty"
      
  },
  "UB9S6E": {
    "title": "HP 2 years Additional Warranty for Color LaserJet Pro MFP M479",
    "price": "19000",
    "image":"https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP.png",
    "duration": "3 year",
    "coverage":"in-warranty"
      
  },
    "U8TP0E": {
    "title": "HP 2 years Additional Color LaserJet Multi Function Printer",
    "price": "24500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Laser-JET-MFP.png",
    "duration": "3 year",
    "coverage":"in-warranty"
      
  },
  "U57D7E": {
    "title": "HP Smart Tank 210 AiO 2 years Additional Warranty",
    "price": "5000",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Smart-tank-AIO-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
      
  },
  "UG467E": {
    "title": "HP OfficeJet Pro 9720 WF AiO 2 years Additional Warranty",
    "price": "8444",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "UG468E": {
    "title": "HP OfficeJet Pro 9730 WF AiO 2 years Additional Warranty",
    "price": "9278",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  
  },
  "UZ275E": {
    "title": "HP OfficeJet Pro 9720 WF AiO 4 years Additional Warranty",
    "price": "16889",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  },
   "UZ276E": {
    "title": "HP OfficeJet Pro 9730 WF AiO 4 years Additional Warranty",
    "price": "19444",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "5 year",
    "coverage":"in-warranty"
  
  },
  "UZ277E": {
    "title": "HP OfficeJet Pro 8120 AiO 4 year Additional Warranty",
    "price": "16111",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Office-jet-Pro-1.png",
    "duration": "5 year",
    "coverage":"in-warranty"
    
  },
 
  "U42GXPE": {
    "title": "HP Neverstop Laser MFP 1200nw 1 year Post Warranty",
    "price": "7500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/12/Neverstop-Laser-MFP.png",
    "duration": "1 year",
    "coverage":"post-warranty"
    
  },
  "U34XRE": {
    "title": "HP Scan jet 2600 2 years Warranty Extension",
    "price": "11800",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/12/HP-Scanjet-2600.png",
    "duration": "3 year",
    "coverage":"in-warranty"
  },
  "U9MW4PE": {
    "title": "HP LaserJet Enterprise M607 M610 1 year Post Warranty",
    "price": "20963",
    "image":"https://arminfoserve.com/wp-content/uploads/2023/12/LaserJet.png",
    "duration": "1 year",
    "coverage":"post-warranty"
  }

}
                                        

def calculate_remaining_days(end_date_str):
    try:
        end_date = datetime.strptime(end_date_str, "%B %d, %Y").date()
        today = datetime.today().date()

        if end_date < today:
            return "0 Days"

        total_days = (end_date - today).days
        years = total_days // 365
        months = (total_days % 365) // 30
        days = (total_days % 365) % 30

        parts = []
        if years > 0:
            parts.append(f"{years} Year{'s' if years > 1 else ''}")
        if months > 0:
            parts.append(f"{months} Month{'s' if months > 1 else ''}")
        if days > 0:
            parts.append(f"{days} Day{'s' if days > 1 else ''}")

        return ", ".join(parts) if parts else "0 Days"
    except Exception:
        return "N/A"

def run_warranty_check(serial_number, product_number=None, eosl_data=eosl_data):

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service, options=options)

    wait = WebDriverWait(driver, 7)

    try:
        driver.get("https://support.hp.com/in-en/check-warranty")

        try:
            btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Accept All Cookies')]")
            ))
            btn.click()
        except Exception as e:
            print("Error while selecting cookies:", e)


        sn_input = wait.until(EC.presence_of_element_located((By.ID, "inputtextpfinder")))
        sn_input.clear()
        sn_input.send_keys(serial_number)

        submit = driver.find_element(By.CLASS_NAME, "button-box")
        driver.execute_script("arguments[0].removeAttribute('disabled')", submit)
        submit.click()
        time.sleep(5)
        
        need_pn = driver.find_elements(By.XPATH,
            "//p[contains(@class,'errorTxt') and contains(text(),'cannot be identified')]"
        )
        if need_pn:
            if not product_number:
                return {"error": "Please enter the product number."}
            pn_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.productNumField.input-box")))
            pn_input.clear()
            pn_input.send_keys(product_number)
            btn2 = driver.find_element(By.ID, "FindMyProductNumber")
            driver.execute_script("arguments[0].removeAttribute('disabled')", btn2)
            btn2.click()
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-info-text h2")))

        name_el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-info-text h2")))
        product_name = driver.execute_script("return arguments[0].innerText;", name_el).strip()

        try:
            info = driver.find_element(By.CSS_SELECTOR, "div.serial-product-no")
            text = driver.execute_script("return arguments[0].innerText;", info)
            m = re.search(r"[Pp]roduct\s*:\s*(\S+)", text)
            extracted_product_number = m.group(1).strip() if m else ""
        except:
            extracted_product_number = ""

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.product-image")))
            img_el = driver.find_element(By.CSS_SELECTOR, "img.product-image")
            image_url = img_el.get_attribute("src")
        except:
            image_url = ""

        sections = driver.find_elements(By.CLASS_NAME, "info-section")
        warranty_data = None
        carepack_active = False

        for sec in sections:
            items = sec.find_elements(By.CLASS_NAME, "info-item")
            data = {}
            for it in items:
                try:
                    lbl = it.find_element(By.CLASS_NAME, "label").text.strip()
                    val = it.find_element(By.CLASS_NAME, "text").text.strip()
                    data[lbl] = val
                except Exception as e:
                    print("Error while extracting info-item:", e)


            cov = data.get("Coverage type", "").lower()
            sts = data.get("Status", "").lower()
            service_type = data.get("Service type", "").lower()

            if cov in ["care pack", "contract","bundled warranty"] and sts in ["active","coverage expiring","upcoming"] and service_type:
                warranty_data = data
                carepack_active = True
                break

            if not carepack_active and cov == "factory warranty" and any(
                k in service_type for k in ("hardware maintenance", "hardware replacement")
            ):
                warranty_data = data
        
        # care_packs = []
        

        addon_text = None
        actual_service_level = "Unknown" 
        if carepack_active:
            addon_parts = []
            for sec in sections:
                items = sec.find_elements(By.CLASS_NAME, "info-item")
                for it in items:
                    try:
                        label = it.find_element(By.CLASS_NAME, "label").text.strip().lower()
                        if label in ["service level", "deliverables"]:
                            text_div = it.find_element(By.CLASS_NAME, "text")
                            text_content = text_div.text.strip().lower()
                            if label == "service level" and actual_service_level == "Unknown":
                                actual_service_level = text_div.text.strip()
                            accidental_matches = re.findall(r"\b(accidental[^\n,]*)", text_content, re.IGNORECASE)
                            for match in accidental_matches:
                                cleaned = match.strip().title()
                                if cleaned not in addon_parts:
                                    addon_parts.append(cleaned)
                            defective_matches = re.findall(r"\b(defective[^\n,]*)", text_content, re.IGNORECASE)
                            for match in defective_matches:
                                cleaned = match.strip().title()
                                if cleaned not in addon_parts:
                                    addon_parts.append(cleaned)
                    except:
                        continue
            if addon_parts:
                addon_text = ", ".join(addon_parts)

        def parse_date(date_input):
            if isinstance(date_input, datetime):
                return date_input
            if isinstance(date_input, date):
                return datetime.combine(date_input, datetime.min.time())
            if isinstance(date_input, str):
                try:
                    return datetime.strptime(date_input.strip(), "%B %d, %Y")
                except ValueError:
                    try:
                        return datetime.strptime(date_input.strip(), "%Y-%m-%d")
                    except Exception as e:
                        print(f"⚠️ Date parse error for '{date_input}': {e}")
                        return None
                    print(f"⚠️ Unsupported date format: {date_input}")
                    return None


         
        def carepack_duration(start_date, end_date):
            try:
                start_date_obj = datetime.strptime(start_date, "%B %d, %Y")
                end_date_obj = datetime.strptime(end_date, "%B %d, %Y")
                delta = relativedelta(end_date_obj, start_date_obj)
                return delta.years, delta.months
            except Exception as e:
                print("❌ Error parsing start/end date:", e)
                return None, None
                    
        start_date_obj = datetime.strptime(warranty_data["Start date"], "%B %d, %Y").date()
        end_date_obj = datetime.strptime(warranty_data["End date"], "%B %d, %Y").date()
        today = datetime.today().date()
        span = relativedelta(end_date_obj, start_date_obj)
        years, months = span.years, span.months
        
        result = {}
        def is_eligible_by_span(years,months,duration_str,addon_text,part_sku,plan_cov,warranty_status,product_number,eosl_data,end_date,actual_service_level,coverage_type,result,):
            dur          = duration_str.strip().lower()
            has_adp = str(addon_text).strip().lower() not in ("", "none", "null")
            sku          = part_sku.upper()
            cov          = plan_cov.strip().lower()
            sts          = warranty_status.strip().lower()
            total_months = years * 12 + months
            today        = datetime.today().date()
            is_3yr_span = (years == 3 and months == 0) or (total_months >= 35)
            is_carepack = coverage_type.strip().lower() == "care pack"
            has_no_addon = not has_adp
            is_in_warranty = cov == "in-warranty"
            has_next_coverage_day = "next coverage day" in actual_service_level.lower()
            print("🔍 Strict Check:")
            print(f"  - is_3yr_span: {is_3yr_span}")
            print(f"  - is_carepack: {is_carepack}")
            print(f"  - has_no_addon: {has_no_addon}")
            print(f"  - is_in_warranty: {is_in_warranty}")
            print(f"  - has_next_coverage_day: {has_next_coverage_day}")
            print(f"  - SKU: {sku} | Coverage: {cov}")
            if has_next_coverage_day:
                print("ℹ️ Detected 'Next Coverage Day' in service level")
                if dur == "1 year" and cov == "post-warranty":
                    result.update({
                        "sku": sku,
                        "duration": dur,
                        "coverage_type": "Post Warranty",  # ✅ This is what you want in final output
                        "reason": "strict_1yr_post_warranty",
                        "plan_source": "strict",
                        
                        })
                    return False
                
                if is_3yr_span and is_carepack and has_no_addon:
                    if sku == "U9WX1E" and is_in_warranty:
                        result.update({
                            "sku": sku,
                            "duration": dur,
                            "coverage_type": "Care Pack",
                            "reason": "strict_3yr_u9wx1e",
                            "plan_source": "strict"
                            })
                        return result
                    # if dur == "1 year" and cov == "post-warranty":
                    #     result.update({
                    #         "sku": sku,
                    #         "duration": dur,
                    #         "coverage_type": "Post Warranty",  # ✅ override here
                    #         "reason": "strict_1yr_post_warranty",
                    #         "plan_source": "strict"
                    #         })
                    #     return result

 
                    print(f"❌ Blocked: SKU {sku} is not eligible (not U9WX1E or post-warranty)")
                    return False  # ✅ STOP — strict failed
                else:
                    print("❌ Blocked: Strict 3-year check not satisfied with 'Next Coverage Day'")
                    return False  # ✅ STOP — not a 3-year sp




            print(f"📦 Plan: {sku} | dur: {dur} | cov: {cov} | status: {sts} | addon: {addon_text}")
            if dur == "1 year" and cov == "post-warranty":
                eosl_str = eosl_data.get(product_number)
                if not eosl_str:
                    # print(f"❌ Skipping plan {sku} - EOSL date not found for {product_number}")
                    return False
                try:
                    eosl_date = datetime.strptime(eosl_str, "%d-%m-%Y").date()
                    if (eosl_date - today).days < 0:
                        # print(f"❌ Skipping plan {sku} - EOSL expired on {eosl_date}")
                        return False
                except Exception as e:
                    # print(f"❌ Failed to parse EOSL date for product {product_number}: {e}")
                    return False
               


            if 11 <= total_months < 15:
                if sku == "U9WX1E":
                    return (cov == "in-warranty") and (sts in ("active", "coverage expiring")) and (not has_adp)


                # Active/expiring: only in-warranty plans, any of 1/2/3 year
                if sts in ("active", "coverage expiring"):
                    if cov !="in-warranty":
                        return False
                    return dur in ("1 year","2 year","3 year")

                # Expired: now allow post-warranty or 3-year based on 2-yr anniversary proximity
                if sts == "expired":
                    # time until 2-year mark
                    two_year_ann = end_date + timedelta(days=730)
                    days_to_2yr  = (two_year_ann - today).days
                    if 90 < days_to_2yr < 365:
                        # more than a year away from 2-year mark
                        return dur in ("3 year")

                    if 0 < days_to_2yr < 90:
                        # within 3 months of 2-year mark
                        return (dur == "3 year") or (cov == "post-warranty")
                    if days_to_2yr >= 365:
                        # more than a year away from 2-year mark
                        return dur in ("2 year","3 year")
                    if days_to_2yr < 0: 
                        # more than a year away from 2-year mark
                        return dur in ("1 year") and (cov == "post-warranty")
                return False
              

            # 15–23 months: 2- and 3-year plans (never add-on)
            elif 15 <= total_months < 23:
                return cov == "in-warranty" and sku != "U9WX1E" and dur in ("2 year", "3 year")

            # 23–35 months: only 3-year plans (never add-on)
            elif 23 <= total_months < 35:
                return cov == "in-warranty" and sku != "U9WX1E" and dur == "3 year"

           
            elif total_months >= 35:
                # EOSL 1-year plan condition
                eosl_ok = False
                eosl_str = eosl_data.get(product_number)
                if eosl_str:
                    try:
                        eosl_date = datetime.strptime(eosl_str, "%d-%m-%Y").date()
                    except Exception:
                        pass
                    else:
                        days_remaining = (end_date - today).days
                        if (
                            0 <= (eosl_date - today).days <= 365
                            and sts in ("active", "coverage expiring","expired")
                            and days_remaining < 90
                            and cov == "post-warranty"
                            and dur == "1 year"
                        ):
                            eosl_ok = True
                adp_ok = (
                  (not has_adp)
                  and sku == "U9WX1E"
                  and cov == "in-warranty"
                  and sts in ("active", "coverage expiring",)
                  )
                print(f"🧪 EOSL_OK={eosl_ok}, ADP_OK={adp_ok}, TotalMonths={total_months}, HasADP={has_adp}")
                return eosl_ok or adp_ok
            return False
        
            
        def is_eligible_printer_span(years, months, duration_str, plan_cov, warranty_status, product_number, eosl_data, end_date):
            dur = duration_str.strip().lower().replace("years", "year").replace(" ", "")
            cov = plan_cov.strip().lower().replace(" ", "")
            sts = warranty_status.strip().lower()
            today = datetime.today().date()
            total_months = years * 12 + months
            # if total_months < 11:
            #     if sts in ("active", "coverage expiring"):
            #         return dur in ("3year", "5year")
            if 11 <= total_months < 15:
                if sts in ("active", "coverage expiring"):
                    return dur in ("3year", "5year")
                if sts == "expired":
                    two_year_ann = end_date + timedelta(days=730)
                    days_to_2yr = (two_year_ann - today).days
                    if days_to_2yr > 0:
                        return dur in ("3year", "5year") or cov == "post-warranty"
                    if days_to_2yr < 0:
                        return dur == "5year" or cov == "post-warranty"
                    return False
            elif 15 <= total_months < 23:
                    if sts in ("active", "coverage expiring"):
                        return cov == "in-warranty" and dur in ("3year", "5year")
                    if sts == "expired":
                        one_year_ann = end_date + timedelta(days=365)
                        days_to_1yr = (one_year_ann - today).days
                        if days_to_1yr > 0:
                            return dur in ("3year", "5year") or cov == "post-warranty"
                        if days_to_1yr < 0:
                            return dur == "5year" or cov == "post-warranty"
                        return False
            elif 23 <= total_months < 35:
                        return cov == "in-warranty" and dur == "5year"
            elif 35 <= total_months < 59:
                        return cov == "in-warranty" and dur == "5year"
            return False
        care_packs = []
        added_parts = set()
        if extracted_product_number in printer_mapping:
            warranty_status = warranty_data.get("Status", "").strip().lower()
            plan_cov = warranty_data.get("Coverage type", "").strip().lower()
            end_date_str = warranty_data.get("End date")
            start_date_str = warranty_data.get("Start date")
            mapped = printer_mapping[extracted_product_number]
            print(f"🔍 Found printer mapping for {extracted_product_number}")
            for mapped_duration in ["2 yr add WE", "4 yr add WE", "1 yr PW"]:
                if mapped_duration in mapped:
                    entries = mapped[mapped_duration]
                    if isinstance(entries, dict):
                        entries = [entries]
                        for entry in entries:
                            part = entry.get("part")
                            if part and part not in added_parts:
                                slug = product_page_mapping.get(part)
                                details = product_title_mapping.get(part.upper(), {})
                                print(f"🔍 DEBUG: Details fetched for {part}: {details}")
                                title = details.get("title")
                                price = details.get("price")
                                image = details.get("image")
                                tag = details.get("tag")
                                duration = details.get("duration", "").strip().lower()  # → ""
                                coverage = details.get("coverage", "").strip().lower()
                                if not all([duration, coverage, title, price, image, slug]):
                                    print(f"🔎 Part={part}, duration={duration}, coverage={coverage}, title={title}, price={price}, image={image}, slug={slug}")
                                    continue
                                is_eligible = is_eligible_printer_span(
                                    years, months, duration, coverage, warranty_status,
                                    extracted_product_number, eosl_data, end_date_obj
                                    )
                                print(f"🧪 {part} eligibility → {is_eligible}")
                                if is_eligible:
                                    care_packs.append({
                                        "label": f"{mapped_duration.upper()} Care Pack",
                                        "part": part,
                                        "title": title,
                                        "price": price,
                                        "image": image,
                                        "tag": tag,
                                        "url": f"https://arminfoserve.com/product/{slug}/"
                                        })
                                    added_parts.add(part)
        


        def is_commercial_model(name: str) -> bool:
            kws = [
                "240","247", "245", "255", "250", "340", "345", "350", "355",
                "elitedesk", "prodesk", "microtower",
                "probook", "elitebook", "zbook", "pro"
                ]
            name_clean = re.sub(r"[^\w\s]", "", name.lower())  # remove punctuation
            return any(kw in name_clean for kw in kws)
        def is_3_year_base_factory_warranty(start_date, end_date, coverage_type):
            if coverage_type.strip().lower() != "factory warranty":
                return False
            diff = relativedelta(end_date, start_date)
            total_months = diff.years * 12 + diff.months
            print(f"📏 Calculated Warranty Duration: {total_months} months")
            return 35 <= total_months <= 37  # allowing ±1 month
        def matches_base_warranty_text(text: str, years: int) -> bool:
            pattern = rf"\b{years}\s*year\s*base\s*warranty\b"
            return re.search(pattern, text.lower()) is not None
        def is_eligible_commercial_span(years, months, duration_str, addon_text, part_sku,
                                        plan_cov, warranty_status, product_number,
                                        eosl_data, end_date, start_date):  # added start_date
            dur = duration_str.strip().lower()
            sku = part_sku.upper()
            cov = plan_cov.strip().lower()
            sts = warranty_status.strip().lower()
            total_months = years * 12 + months
            today = datetime.today().date()
            print(f"📦 Plan: {sku} | dur: {dur} | cov: {cov} | status: {sts} | addon: {addon_text}")
            is_3yr_base = is_3_year_base_factory_warranty(start_date, end_date, plan_cov)
            dur_lower = (dur or "").lower().strip()
            title_lower = (title or "").lower().strip()
            start = parse_date(start_date)
            end = parse_date(end_date)
            is_3yr_base = (
                coverage_type.strip().lower() == "factory warranty" and
                (end - start).days >= 1000
                )
            if not is_3yr_base and re.search(r"\b3\s*year\s*(base|factory)\s*warranty\b", title_lower):
                print(f"❌ Skipping: {part} is for 3-year base warranty but product has 1-year base warranty")
                return False
            if is_3yr_base and re.search(r"\b1\s*year\s*(base|factory)\s*warranty\b", title_lower):
                print(f"❌ Skipping: {part} is for 1-year base warranty but product has 3-year base warranty")
                return False



         


            if 11 <= total_months < 15:
                if sts in ("active", "coverage expiring"):
                    if cov != "in-warranty":
                        return False
                    return dur in ("1 year", "2 year", "3 year", "5 year")
                if sts == "expired":
                    five_year_ann = start_date + timedelta(days=1460)
                    days_to_5yr = (five_year_ann - today).days
                    if 90 < days_to_5yr <= 730:
                        return dur in ("3 year", "5 year")
                    if 0 < days_to_5yr < 90:
                        return dur == "5 year" or (dur == "1 year" and cov == "post-warranty")
                    if days_to_5yr > 730:
                        return dur in ("3 year", "5 year")
                    if days_to_5yr < 0:
                        return dur == "1 year" and cov == "post-warranty"
                return False
            if 15 <= total_months < 23:
                return cov == "in-warranty" and  dur in ("2 year", "3 year", "5 year")
            if 23 <= total_months < 35:
                return cov == "in-warranty" and  dur in ("3 year", "5 year")
            if 35 <= total_months < 59:
                return cov == "in-warranty" and  dur == "5 year"
            if total_months >= 59:
                eosl_ok = False
                eosl_str = eosl_data.get(product_number)
                if eosl_str:
                    try:
                        eosl_date = datetime.strptime(eosl_str, "%d-%m-%Y").date()
                    except Exception:
                        pass
                    else:
                        days_remaining = (end_date - today).days
                        if (
                            0 <= (eosl_date - today).days <= 365 and
                            sts in ("active", "coverage expiring", "expired") and
                            days_remaining <= 90 and
                            cov == "post-warranty" and
                            dur == "1 year"
                            ):
                            eosl_ok = True
                            print(f"🧪 EOSL_OK={eosl_ok}, TotalMonths={total_months}")
                            return eosl_ok
                        return False
                        

        # 1. Extract actual warranty data fields
        actual_start_date = warranty_data.get("Start date")
        actual_end_date = warranty_data.get("End date")
        actual_status = warranty_data.get("Status", "")
        actual_coverage_type = warranty_data.get("Coverage type", "")
        actual_coverage = warranty_data.get("Coverage", "")
        addon_parts = warranty_data.get("Add-on", "")
        years, months = carepack_duration(actual_start_date, actual_end_date)
        if years is None or months is None:
            return {"error": "Warranty dates could not be parsed."}
    
            
        if warranty_data and warranty_data.get("End date"):
            remaining_days = calculate_remaining_days(warranty_data.get("End date"))
        else:
            remaining_days = None
        name = product_name.lower().strip()
        rules = [
            {
                "includes": ["hp laptop", "x360 14", "chromebook 11", "15", "15s"],
                "excludes": ["pavilion", "victus", "omen", "envy", "spectre", "x360", "chromebook", "notebook"],
                "parts": ["U8LH7PE", "U8LH8E", "U8LJ4E", "UN008E", "UB5R2E", "U8LH3E", "U8LH9E","U9WX1E"]
            },
            {
              "includes": ["15s"],
              "excludes": [],
              "parts": ["U8LH7PE", "U8LH8E", "U8LJ4E","UB5R2E", "UN008E",  "U8LH3E", "U8LH9E","U9WX1E"]
            },
            {
                "includes": ["pavilion"],
                "excludes": ["All-", "Desktop"],
                "parts": ["U0H90E", "U6WD1E", "UN009E", "UB5R3E", "UN006E", "U0H96E", "U0H93PE","U9WX1E"]
            },
             
            {
                "includes": ["victus"],
                "excludes": ["all-"],
                "parts": ["U0H90E", "U6WD1E", "UN009E", "UB5R3E", "UN006E", "U0H96E", "U0H93PE","U9WX1E"],
                    
            }, 
            {
                "includes": ["omen"],
                "excludes": ["All|desktop"],
                "parts": ["U0H91E", "U6WD2E", "UN010E", "UB5R4E", "UN007E", "U6WC9E", "UN082PE"], 
            },
            {
                "includes": ["omnibook"],
                "excludes": ["All|desktop"],
                "parts": ["U0H91E", "U6WD2E", "UN010E", "UB5R4E", "UN007E", "U6WC9E", "UN082PE"], 
            },
            
            {
                "includes": ["envy"],
                "excludes": ["all-"],
                "parts": ["U0H91E", "U6WD2E", "UN010E", "UB5R4E", "UN007E", "U6WC9E", "UN082PE","U9WX1E"], 
            },
            {
                "includes": ["spectre"],
                "excludes": ["all-"],
                "parts": ["U0H92E", "U6WD3E", "UM952E", "UN011E", "U6WD0E", "UB5R5E", "U0H94PE","U9WX1E"],
            },
            {
                "includes": ["240|245|255|250|340|345|350|355"],
                "excludes": ["all-"],
                "parts": ["U9BA7E", "U9BA3E", "U9AZ7E", "U9BA9E", "U9EE8E", "UB5U0E", "U9BB1PE","U22N8E"],
            },
            {
                "includes": ["zbook"],
                "excludes": ["All|MFP"],
                "parts": ["U02BVE", "U02BSE", "U10KHE"]
            },

            {
                "includes": ["(?i)chromebook"],
                "excludes": [],
                "parts": ["U8LH7PE", "U8LH8E", "U8LJ4E", "UN008E", "UB5R2E", "U8LH3E", "U8LH9E"],
            },
            {
                "includes": ["(?i)Elitebook 8|Elitebook 7"],
                "excludes": ["(?i)All|MFP"],
                "parts": ["UC279E", "U4391E", "UC282E", "U7861E", "UB5T7E", "U7876E"],
            },
            {
                "includes": ["(?i)Elitebook 1|EliteBook x360 1030"],
                "excludes": ["(?i)All|MFP"],
                "parts": ["UB0E2E", "UB0E6E"],
            },
               
            {
                "includes": ["hp all-in-one", "slim", "desktop pc m"],
                "excludes": ["victus", "omen", "envy", "spectre", "printer"],
                "parts": ["UJ217E"]
            },
            {
                "includes": ["(?i)ProBook 440|ProBook 445|ProBook 455|ProBook 450|ProBook 430"],
                "excludes": ["(?i)All|MFP"],
                "parts": ["UK703E","U86DXE","UK744E", "UK726E","U86E0E","U86DVE","UK718E", "UK749E", "UB8B3E", "UK738PE", "UB8B6E"],
            },
            {
                "includes": ["(?i)HP all-in-one|slim|Desktop PC M|280"],
                "excludes": ["(?i)Victus|Omen|Envy|Spectre|printer"],
                "parts": ["U5864PE", "U6578E", "U7899E", "U0A84E", "UF236E", "U0A83E", "UF360E", "U7923E", "U7925E", "UF361E", "U7897E", "U0A85E", "U11BVE"],

            },
            {
                "includes": [ "(?i)elitedesk|prodesk|Microtower"],
                "excludes": ["(?i)200|Victus|Omen|Envy|Spectre|printer"],
                "parts": ["UJ217E", "U4813PE"],

            },
            {
                "includes": ["(?i)Pavilion all|Pavilion 3|pavilion gaming d"],
                "excludes": [],
                "parts": ["U4813PE", "UA055E"],
            },
            {
                "includes": ["(?i)Envy all|gaming desktop"],
                "excludes": ["(?i)Pavilion|Victus"],
                "parts": ["UA055E", "UN062PE"],
            },
            {
                "includes": ["zbook g10"],
                "excludes": ["all-"],
                "parts": ["U60ZBE", "U60ZCE", "U60ZWE", "U60ZXE", "U61E2E"],
            },
            {
                "includes": [ "(?i)HP P2|HP e2"],
                "excludes": [],
                "parts": ["U7935E", "U4925PE", "U7937E", "U4936PE"],
            },
            {
                "includes": ["workstation 600", "workstation 400"],
                "excludes": ["pavilion", "victus", "omen", "envy", "spectre", "x360", "chromebook", "notebook", "hp laptop", "15", "15s", "desktop", "all-in-one", "zbook", "monitor"],
                "parts": ["U7944E", "U7942E", "U1G57E", "U1G39E", "U1G37E"]             
            }



        ]
        

        for rule in rules:
            includes_match = all(re.search(kw, name) for kw in rule.get("includes", []))
            excludes_match = any(re.search(exc, name) for exc in rule["excludes"])
            if includes_match and not excludes_match:
                try:
                    start_date_str = warranty_data.get("Start date")
                    end_date_str = warranty_data.get("End date")
                    years, months = carepack_duration(start_date_str, end_date_str)

                except Exception as e:
                    print("❌ Error parsing warranty duration:", e)
                    years = None
                    months = None

                for part in rule["parts"]:
                    slug = product_page_mapping.get(part)
                    details = product_title_mapping.get(part, {})
                    title = details.get("title")
                    price = details.get("price")
                    image = details.get("image")
                    tag = details.get("tag")
                    coverage = details.get("coverage", "")
                    duration = details.get("duration", "")
                    status = warranty_data.get("Status", "")
                    service_level = actual_service_level  # ✅ correctly parsed from DOM
                    coverage_type = warranty_data.get("Coverage type", "")
                    end_date = warranty_data.get("End date")
                    plan_cov      = details.get("coverage", "")
                    warranty_stat = warranty_data.get("Status", "")
                    product_num   = extracted_product_number
                    name_low = product_name.lower()
                    commercial = is_commercial_model(product_name)

                    print(f"🧪 Product name to check commercial: '{product_name}' → {product_name.lower().split()}")
                    if is_commercial_model(product_name):
                      print("💼 Commercial device detected. Using commercial span logic.")
                      ok = is_eligible_commercial_span(years, months, duration, addon_text, part,plan_cov, warranty_stat, product_num,eosl_data, end_date_obj,start_date_obj)
                    else:
                        print("🧑‍💻 Consumer device. Using consumer logic with ADP check.")
                        ok = is_eligible_by_span(years, months,duration, addon_text, part,plan_cov, warranty_stat,product_num, eosl_data,end_date_obj,actual_service_level,coverage_type,result) 
                    print(f"📦 Plan: {part} | dur: {duration} | cov: {coverage} | status: {status} | addon: {addon_text}")

                    if ok and slug:
                      print(f"✅ MATCHED: {part} added as eligible care pack")
                      care_packs.append({
                            "label": "Recommended Care Pack",
                            "part": part,
                            "title": title,
                            "price": price,
                            "image": image,
                            "tag": tag,
                            "url": f"https://arminfoserve.com/product/{slug}/"
                        })
                        
       
                if not care_packs:
                    actual_service_level = warranty_data.get("Service level", "")
                    actual_status = warranty_data.get("Status", "")
                    actual_coverage = warranty_data.get("Coverage", "")
                    actual_coverage_type = warranty_data.get("Coverage Type", "")
                    product_number = warranty_data.get("Product Number", "")
        

        current_date_str = datetime.today().strftime("%B %d, %Y")

        if warranty_data:
            return {
                "product_name": product_name,
                "product_number": extracted_product_number,
                "coverage_type": warranty_data.get("Coverage type"),
                "start_date": warranty_data.get("Start date"),
                "end_date": warranty_data.get("End date"),
                "status": warranty_data.get("Status"),
                "image_url": image_url,
                "remaining_days": remaining_days if remaining_days is not None else "N/A",
                "current_date": current_date_str,
                "care_packs": care_packs,
                "result":result,
                "actual_service_level": actual_service_level,
                # "eosl_date": eosl_date,
                "addon": addon_text
                
            }
        else:
            return {"error": "No valid warranty information found."}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()




        
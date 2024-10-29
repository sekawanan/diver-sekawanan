from enum import Enum

class GenderEnum(str, Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    PREFER_NOT_TO_SAY = 'Prefer not to say'
    ATTACK_APACHE_HELICOPTER = 'Attack Apache Helicopter'

class CertificationEnum(str, Enum):
    OPEN_WATER = 'Open Water'
    ADVANCED_OPEN_WATER = 'Advanced Open Water'
    RESCUE_DIVER = 'Rescue Diver'
    DIVE_MASTER = 'Dive Master'
    DIVE_INSTRUCTOR = 'Dive Instructor'

class CertificationIssuerEnum(str, Enum):
    PADI = 'PADI'
    SSI = 'SSI'
    POSSI = 'POSSI'
    OTHER = 'Other'

class WantToSeeEnum(str, Enum):
    CORALS = 'Corals'
    MACRO = 'Macro'
    PELAGIC = 'Pellagic'
    OTHER = 'Other'

class DiveConditionEnum(str, Enum):
    INDEPENDENT = 'I can be independent'
    NEED_HELP = 'I need help'
    PREFER_NOT_DIVE = 'I prefer not to dive in current'
    OTHER = 'Other'

class BottomTimeEnum(str, Enum):
    UNDER_30 = 'Under 30 minutes'
    BETWEEN_31_40 = '31-40 minutes'
    BETWEEN_41_50 = '41-50 Minutes'
    BETWEEN_51_60 = '51-60 Minutes'
    MORE_THAN_60 = 'More than 60 minutes'
    OTHER = 'Other'

class TroubleEqualizingEnum(str, Enum):
    NEVER = 'Never'
    SOMETIMES = 'Sometimes'
    OFTEN = 'Often'
    ALWAYS = 'Always'
    OTHER = 'Other'
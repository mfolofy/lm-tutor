"""
credential-electrician grader — computation-heavy checks for electrical standards.

Layer 2 validations that require cross-text analysis beyond single-line regex.

Current graders:
  - nec-citation-validity: Confirms that NEC article references cited by the
    model actually exist and are used in the correct context.
  - disclaimer-presence: Verifies that model outputs containing electrical
    installation advice include a proper disclaimer.

Usage (called by the Layer 1 harness after regex checks pass):
    from tutor.classes.credential_electrician.grader import grade_credential_electrician
    results = grade_credential_electrician(submission_text, metadata={})
"""

from __future__ import annotations

import re
from typing import Any

# ── DISCLAIMER CHECK ────────────────────────────────────────────────────────

ELECTRICAL_ADVICE_TRIGGERS = re.compile(
    r"(?i)\b(?:wire|circuit|breaker|panel|conduit|install|ground|bond|"
    r"ampacity|voltage|current|load|conductor|switch|receptacle|outlet|"
    r"disconnect|service|feeder|branch|GFCI|AFCI)\b"
)

REQUIRED_DISCLAIMER_PHRASES = [
    r"(?i)licensed\s+electrician\s+(?:should|must|needs?\s+to)",
    r"(?i)consult\s+(?:a\s+)?(?:licensed\s+)?electrician",
    r"(?i)(?:for\s+)?(?:educational|informational)\s+purposes\s+only",
    r"(?i)verify\s+(?:with|in accordance\s+with)\s+(?:the\s+)?(?:NEC|local\s+code)",
]


def _has_disclaimer(text: str, phrases: list[str]) -> bool:
    """Check if the text contains at least one of the required disclaimer phrases."""
    return any(re.search(p, text) for p in phrases)


def grade_disclaimer_presence(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Grade whether electrical installation advice includes a required disclaimer.

    Returns a dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    has_advice = bool(ELECTRICAL_ADVICE_TRIGGERS.search(text))

    if not has_advice:
        return {
            "pass": True,
            "reason": "No electrical terms detected; disclaimer not required.",
            "matches": [],
        }

    has_disclaimer = _has_disclaimer(text, REQUIRED_DISCLAIMER_PHRASES)

    if has_disclaimer:
        return {
            "pass": True,
            "reason": "Required electrical disclaimer present.",
            "matches": [],
        }

    return {
        "pass": False,
        "reason": (
            "Electrical installation advice detected without required disclaimer. "
            "Include: 'For educational purposes only. Consult a licensed electrician "
            "for all electrical work. Verify all information with the NEC and local codes.'"
        ),
        "matches": [],
    }


# ── NEC CITATION VALIDITY ───────────────────────────────────────────────────

# Canonical NEC articles (article number -> description)
KNOWN_NEC_REFERENCES: dict[str, str] = {
    "90": "Introduction (AHJ authority, enforcement, purpose)",
    "100": "Definitions",
    "110": "General Requirements for Electrical Installations",
    "200": "Use and Identification of Grounded Conductors",
    "210": "Branch Circuits",
    "215": "Feeders",
    "220": "Branch-Circuit, Feeder, and Service Load Calculations",
    "225": "Outside Branch Circuits and Feeders",
    "230": "Services",
    "240": "Overcurrent Protection",
    "245": "Overvoltage Protection",
    "250": "Grounding and Bonding",
    "285": "Surge-Protective Devices (SPDs)",
    "300": "General Wiring Methods",
    "310": "Conductors for General Wiring",
    "312": "Cabinets, Cutout Boxes, and Meter Socket Enclosures",
    "314": "Outlet, Device, Pull, and Junction Boxes",
    "320": "Armored Cable (AC)",
    "322": "Flat Cable Assemblies (FC)",
    "324": "Flat Conductor Cable (FCC)",
    "326": "Integrated Gas Spacer Cable (IGS)",
    "328": "Medium-Voltage Cable",
    "330": "Metal-Clad Cable (MC)",
    "332": "Mineral-Insulated, Metal-Sheathed Cable (MI)",
    "334": "Nonmetallic-Sheathed Cable (NM)",
    "336": "Power and Control Tray Cable (TC)",
    "338": "Service-Entrance Cable (SE)",
    "340": "Underground Feeder and Branch Circuit Cable (UF)",
    "342": "Intermediate Metal Conduit (IMC)",
    "344": "Rigid Metal Conduit (RMC)",
    "348": "Flexible Metal Conduit (FMC)",
    "350": "Liquidtight Flexible Metal Conduit (LFMC)",
    "352": "Rigid Polyvinyl Chloride Conduit (PVC)",
    "353": "High Density Polyethylene Conduit (HDPE)",
    "354": "Nonmetallic Underground Conduit with Conductors (NUCC)",
    "355": "Reinforced Thermosetting Resin Conduit (RTRC)",
    "356": "Liquidtight Flexible Nonmetallic Conduit (LFNC)",
    "358": "Electrical Metallic Tubing (EMT)",
    "360": "Flexible Metallic Tubing (FMT)",
    "362": "Electrical Nonmetallic Tubing (ENT)",
    "366": "Auxiliary Gutters",
    "368": "Busways",
    "370": "Cablebus",
    "372": "Cellular Concrete Floor Raceways",
    "374": "Cellular Metal Floor Raceways",
    "376": "Metal Wireways",
    "378": "Nonmetallic Wireways",
    "380": "Multioutlet Assemblies",
    "382": "Nonmetallic Extensions",
    "384": "Strut-Type Channel Raceway",
    "386": "Surface Metal Raceways",
    "388": "Surface Nonmetallic Raceways",
    "390": "Underfloor Raceways",
    "392": "Cable Trays",
    "393": "Low-Voltage Suspended Ceiling Power Distribution Systems",
    "394": "Concealed Knob-and-Tube Wiring",
    "396": "Messenger-Supported Wiring",
    "398": "Open Wiring on Insulators",
    "400": "Flexible Cords and Cables",
    "402": "Fixture Wires",
    "404": "Switches",
    "406": "Receptacles, Cord Connectors, and Attachment Plugs (Caps)",
    "407": "Cord-and-Plug-Connected Appliances",
    "408": "Switchboards and Panelboards",
    "409": "Industrial Control Panels",
    "410": "Luminaires, Lampholders, and Lamps",
    "411": "Lighting Systems Operating at 30V or Less",
    "422": "Appliances",
    "424": "Fixed Electrical Space-Heating Equipment",
    "425": "Fixed Resistance and Electrode Industrial Process Heating",
    "426": "Fixed Outdoor Electric Deicing and Snow-Melting Equipment",
    "427": "Fixed Electric Heating Equipment for Pipelines and Vessels",
    "430": "Motors, Motor Circuits, and Controllers",
    "440": "Air-Conditioning and Refrigeration Equipment",
    "445": "Generators",
    "450": "Transformers and Transformer Vaults",
    "460": "Capacitors",
    "470": "Resistors and Reactors",
    "480": "Storage Batteries",
    "490": "Equipment Over 1000V (Nominal)",
    "500": "Hazardous (Classified) Locations, Classes I, II, III",
    "501": "Class I Locations",
    "502": "Class II Locations",
    "503": "Class III Locations",
    "504": "Intrinsically Safe Systems",
    "505": "Class I, Zone 0, 1, and 2 Locations",
    "506": "Zone 20, 21, and 22 Locations for Combustible Dusts",
    "510": "Hazardous (Classified) Locations — Specific",
    "511": "Commercial Garages, Repair and Storage",
    "513": "Aircraft Hangars",
    "514": "Motor Fuel Dispensing Facilities",
    "515": "Bulk Storage Plants",
    "516": "Spray Application, Dipping, Coating, and Printing",
    "517": "Health Care Facilities",
    "518": "Assembly Occupancies",
    "520": "Theaters, Audience Areas of Motion Picture Studios",
    "525": "Carnivals, Circuses, Fairs, and Similar Events",
    "530": "Motion Picture and Television Studios",
    "540": "Motion Picture Projectors",
    "545": "Manufactured Buildings",
    "550": "Mobile Homes, Manufactured Homes, and Mobile Home Parks",
    "551": "Recreational Vehicles and Recreational Vehicle Parks",
    "552": "Park Trailers",
    "553": "Floating Buildings",
    "555": "Marinas, Boatyards, and Commercial Docking Facilities",
    "590": "Temporary Installations",
    "600": "Electric Signs and Outline Lighting",
    "604": "Manufactured Wiring Systems",
    "605": "Office Furnishings",
    "610": "Cranes and Hoists",
    "620": "Elevators, Dumbwaiters, Escalators, Moving Walks",
    "625": "Electric Vehicle Power Transfer System",
    "626": "Electrified Truck Parking Spaces",
    "630": "Electric Welders",
    "640": "Audio Signal Processing, Amplification Equipment",
    "645": "Information Technology Equipment",
    "646": "Modular Data Centers",
    "647": "Sensitive Electronic Equipment",
    "650": "Pipe Organs",
    "660": "X-Ray Equipment",
    "665": "Induction and Dielectric Heating Equipment",
    "668": "Electrolytic Cells",
    "669": "Electroplating",
    "670": "Industrial Machinery",
    "675": "Electrically Driven Irrigation Machines",
    "680": "Swimming Pools, Spas, Hot Tubs, and Similar Installations",
    "682": "Natural and Artificially Made Bodies of Water",
    "685": "Integrated Electrical Systems",
    "690": "Solar Photovoltaic (PV) Systems",
    "691": "Large-Scale Photovoltaic Electric Power Production",
    "692": "Fuel Cell Systems",
    "694": "Wind Electric Systems",
    "695": "Fire Pumps",
    "700": "Emergency Systems",
    "701": "Legally Required Standby Systems",
    "702": "Optional Standby Systems",
    "705": "Interconnected Electric Power Production Sources",
    "706": "Energy Storage Systems",
    "708": "Critical Operations Power Systems (COPS)",
    "710": "Stand-Alone Systems",
    "712": "Direct Current Microgrids",
    "720": "Circuits and Equipment Operating at Less Than 50 Volts",
    "722": "Cables for Portable and Power-Limited Circuits",
    "725": "Class 1, Class 2, and Class 3 Remote-Control, Signaling Circuits",
    "727": "Instrumentation Tray Cable",
    "728": "Fire-Resistive Cable Systems",
    "730": "Energy Management Systems",
    "750": "Energy Management Systems",
    "760": "Fire Alarm Systems",
    "770": "Optical Fiber Cables and Raceways",
    "800": "General Requirements for Communications Systems",
    "805": "Communications Circuits",
    "810": "Radio and Television Equipment",
    "820": "Community Antenna Television and Radio Distribution",
    "830": "Network-Powered Broadband Communications Systems",
    "840": "Premises-Powered Broadband Communications Systems",
}

NEC_REF_PATTERN = re.compile(
    r"\bNEC\s+(\d{3}(?:\.\d+(?:\([A-Z]\))?(?:\([a-zA-Z0-9]\))?)?)",
    re.IGNORECASE,
)


def grade_nec_citations(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Grade NEC reference validity in electrical text.

    Returns a dict with ``pass`` (bool), ``reason`` (str),
    ``valid_refs`` (list), and ``invalid_refs`` (list).
    """
    matches = NEC_REF_PATTERN.findall(text)
    valid: list[str] = []
    invalid: list[str] = []

    for ref_num in matches:
        # Extract the base article number (everything before the first dot,
        # if present, or just the first three characters for simple article refs).
        # The regex captures the full reference string.
        ref = f"NEC {ref_num}"
        # Try the full capture as-is; if it includes subsection,
        # extract the base article number.
        base = ref_num.split(".")[0].strip()
        if base in KNOWN_NEC_REFERENCES:
            valid.append(ref)
        else:
            invalid.append(ref)

    if invalid:
        return {
            "pass": False,
            "reason": f"Unknown NEC reference(s): {', '.join(invalid)}",
            "valid_refs": valid,
            "invalid_refs": invalid,
        }

    return {
        "pass": True,
        "reason": "All NEC references are valid.",
        "valid_refs": valid,
        "invalid_refs": [],
    }


# ── AGGREGATE GRADER ────────────────────────────────────────────────────────


def grade_credential_electrician(
    text: str, metadata: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Run all credential-electrician graders and return results.

    Args:
        text: The submitted model response text.
        metadata: Optional dict with contextual info (e.g. ``{"context": "residential"}``).

    Returns:
        List of result dicts, one per grader, each with:
            grader_id (str): unique identifier
            pass (bool): whether the check passed
            reason (str): explanation
            matches (list): matched items if applicable
    """
    results: list[dict[str, Any]] = []

    disclaimer_result = grade_disclaimer_presence(text, metadata)
    disclaimer_result["grader_id"] = "disclaimer-presence"
    results.append(disclaimer_result)

    nec_result = grade_nec_citations(text, metadata)
    nec_result["grader_id"] = "nec-citation-validity"
    results.append(nec_result)

    return results

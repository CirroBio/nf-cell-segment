#!/usr/local/bin/python3

import json
import logging
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Default channels will be shown in cycles of magenta, cyan, and yellow
color_wheel = [
    [0, 255, 255],
    [255, 0, 255],
    [255, 255, 0]
]

def format_vitessce_segmentation(
    name: str,
    description: str,
    zarr_fp: str,
    image_key: str,
    obs_set_paths: List[str],
    obs_set_names: List[str],
    init_gene: str,
    channel_names: list,
    mask_channels: list,
    schema_version = "1.0.16",
    obs_type = "cell",
    feature_type = "marker",
    spots_key = "cells",
    feature_value_type = "expression"
):
    
    # Set up the channels that will be displayed.
    # Note that this includes the channels which are shown across both spatial plots.
    # Since there are only three colors which can be shown easily, we will only include slots for three channels.
    # That is in addition to the mask channel.
    # The left-hand image will get A, B, C, D, and the right-hand image will get E, F, G, H.
    if "cell" in mask_channels:
        mask_ix = channel_names.index("cell")
    elif "nucleus" in mask_channels:
        mask_ix = channel_names.index("nucleus")
    else:
        raise ValueError("The mask channel must be either 'cell' or 'nucleus'")

    # Find the non-mask channels
    image_ixs = [i for i, c in enumerate(channel_names) if c not in mask_channels]

    return {
        "version": schema_version,
        "name": name,
        "description": description,
        "datasets": [
            {
                "uid": "A",
                "name": name,
                "files": [
                    {
                        "url": zarr_fp,
                        "fileType": "image.spatialdata.zarr",
                        "coordinationValues": {
                            "fileUid": image_key,
                            "obsType": obs_type
                        },
                        "options": {
                            "path": f'images/{image_key}'
                        }
                    }
                ]
            }
        ],
        "coordinationSpace": {
            "dataset": {
                "A": "A"
            },
            "spatialTargetZ": {
                "A": 0
            },
            "spatialTargetT": {
                "A": 0
            },
            "imageLayer": {
                "A": "__dummy__"
            },
            "fileUid": {
                "A": "image"
            },
            "spatialLayerOpacity": {
                "A": 1
            },
            "spatialLayerVisible": {
                "A": True
            },
            "photometricInterpretation": {
                "A": "BlackIsZero"
            },
            "imageChannel": {
                "A": "__dummy__",
                "B": "__dummy__",
                "C": "__dummy__"
            },
            "spatialTargetC": {
                "A": mask_ix,
                "B": image_ixs[0] if len(image_ixs) > 0 else None,
                "C": image_ixs[1] if len(image_ixs) > 1 else None
            },
            "spatialChannelColor": {
                "A": color_wheel[0],
                "B": color_wheel[1],
                "C": color_wheel[2]
            },
            "spatialChannelWindow": {
                "A": None,
                "B": None,
                "C": None
            },
            "spatialChannelVisible": {
                "A": True,
                "B": True,
                "C": True
            },
            "spatialChannelOpacity": {
                "A": 1,
                "B": 1,
                "C": 1
            },
            "metaCoordinationScopes": {
                "A": {
                    "spatialTargetZ": "A",
                    "spatialTargetT": "A",
                    "imageLayer": "A"
                }
            },
            "metaCoordinationScopesBy": {
                "A": {
                    "imageLayer": {
                    "fileUid": {
                        "A": "A"
                    },
                    "spatialLayerOpacity": {
                        "A": "A"
                    },
                    "spatialLayerVisible": {
                        "A": "A"
                    },
                    "photometricInterpretation": {
                        "A": "A"
                    },
                    "imageChannel": {
                        "A": [
                            "A",
                            "B",
                            "C"
                        ]
                    }
                    },
                    "imageChannel": {
                        "spatialTargetC": {
                            "A": "A",
                            "B": "B",
                            "C": "C"
                        },
                        "spatialChannelColor": {
                            "A": "A",
                            "B": "B",
                            "C": "C"
                        },
                        "spatialChannelWindow": {
                            "A": "A",
                            "B": "B",
                            "C": "C"
                        },
                        "spatialChannelVisible": {
                            "A": "A",
                            "B": "B",
                            "C": "C"
                        },
                        "spatialChannelOpacity": {
                            "A": "A",
                            "B": "B",
                            "C": "C"
                        }
                    }
                }
            }
        },
        "layout": [
            {
            "component": "spatialBeta",
                "coordinationScopes": {
                    "dataset": "A",
                    "metaCoordinationScopes": [
                        "A"
                    ],
                    "metaCoordinationScopesBy": [
                        "A"
                    ]
                },
                "x": 0,
                "y": 0,
                "w": 9,
                "h": 12
            },
            {
                "component": "layerControllerBeta",
                "coordinationScopes": {
                    "dataset": "A",
                    "metaCoordinationScopes": [
                        "A"
                    ],
                    "metaCoordinationScopesBy": [
                        "A"
                    ]
                },
                "x": 9,
                "y": 0,
                "w": 3,
                "h": 12
            }
        ],
        "initStrategy": "auto"
    }


def main():
    # Read in the spatialdata.kwargs.json file
    with open("spatialdata.kwargs.json", "r") as f:
        vt_kwargs = json.load(f)

    # Configure the viewer twice, once to show segmentation
    # and a second time to show cell measurements
    for prefix, vt_config in [
        ("segmentation", format_vitessce_segmentation(**vt_kwargs))
    ]:
        # Save the configuration to JSON
        with open(f"{prefix}.vt.json", "w") as f:
            json.dump(vt_config, f, indent=4)


main()
#!/usr/local/bin/python3

import json
import logging
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# All non-mask channels will be shown in cycles of semi-magenta, semi-cyan, and semi-yellow
color_wheel = [
    [0, 128, 128],
    [128, 0, 128],
    [128, 128, 0]
]
semi_white = [128, 128, 128]

# The mask channel (cell outlines) will be shown in semi-white with low transparency
mask_channel = [128, 128, 128]

def format_vitessce(
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
        mask_ix = mask_channels.index("cell")
    elif "nucleus" in mask_channels:
        mask_ix = mask_channels.index("nucleus")
    else:
        raise ValueError("The mask channel must be either 'cell' or 'nucleus'")
    
    # Find the non-mask channels
    image_ixs = [i for i, c in enumerate(channel_names) if c not in mask_channels]

    # Only take the first three non-mask channels
    assert len(image_ixs) >= 3, "There must be at least three non-mask channels to display"
    if len(image_ixs) > 3:
        image_ixs = image_ixs[:3]

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
                    },
                    {
                        "url": zarr_fp,
                        "fileType": "obsFeatureMatrix.spatialdata.zarr",
                        "coordinationValues": {
                            "obsType": obs_type
                        },
                        "options": {
                            "path": "tables/table/X"
                        }
                    },
                    {
                        "url": zarr_fp,
                        "fileType": "obsSpots.spatialdata.zarr",
                        "coordinationValues": {
                            "obsType": obs_type
                        },
                        "options": {
                            "path": f"shapes/{spots_key}",
                            "tablePath": "tables/table"
                        }
                    },
                    {
                        "url": zarr_fp,
                        "fileType": "obsSets.spatialdata.zarr",
                        "coordinationValues": {
                            "obsType": obs_type
                        },
                        "options": {
                            "obsSets": [
                                {
                                    "name": name,
                                    "path": f"tables/table/{path}"
                                }
                                for path, name in zip(obs_set_paths, obs_set_names)
                            ]
                        }
                    }
                ]
            }
        ],
        "coordinationSpace": {
            "dataset": {
                "A": "A"
            },
            "featureSelection": {
                "A": [init_gene],
                "B": [init_gene]
            },
            "obsType": {
                "A": obs_type
            },
            "featureType": {
                "A": feature_type
            },
            "featureValueType": {
                "A": feature_value_type
            },
            "obsColorEncoding": {
                "A": "cellSetSelection",
                "B": "geneSelection"
            },
            "spatialTargetZ": {
                "A": 0
            },
            "spatialTargetT": {
                "A": 0
            },
            "imageLayer": {
                "A": "__dummy__",
                "B": "__dummy__"
            },
            "fileUid": {
                "A": image_key,
                "B": image_key
            },
            "spatialLayerOpacity": {
                "A": 1,
                "B": 0.5,
                "C": 1,
                "D": 0.5
            },
            "spatialLayerVisible": {
                "A": True,
                "B": True,
                "C": True,
                "D": True
            },
            "photometricInterpretation": {
                "A": "BlackIsZero",
                "B": "BlackIsZero"
            },
            "imageChannel": {
                "A": "__dummy__",
                "B": "__dummy__"
            },
            "spatialTargetC": {
                "A": mask_ix,
                "B": image_ixs[0],
                "C": image_ixs[1],
                "D": image_ixs[2],
                "E": mask_ix,
                "F": image_ixs[0],
                "G": image_ixs[1],
                "H": image_ixs[2]
            },
            "spatialChannelColor": {
                "A": semi_white,
                "B": color_wheel[0],
                "C": color_wheel[1],
                "D": color_wheel[2],
                "E": semi_white,
                "F": color_wheel[0],
                "G": color_wheel[1],
                "H": color_wheel[2]
            },
            "spatialChannelWindow": {
                "A": None,
                "B": None,
                "C": None,
                "D": None,
                "E": None,
                "F": None,
                "G": None,
                "H": None
            },
            "spatialChannelVisible": {
                "A": True,
                "B": True,
                "C": True,
                "D": True,
                "E": True,
                "F": True,
                "G": True,
                "H": True
            },
            "spatialChannelOpacity": {
                "A": 0.25,
                "B": 0.75,
                "C": 0.75,
                "D": 0.75,
                "E": 0.25,
                "F": 0.75,
                "G": 0.75,
                "H": 0.75
            },
            "spotLayer": {
                "A": "__dummy__",
                "B": "__dummy__"
            },
            "spatialSpotRadius": {
                "A": 20,
                "B": 20
            },
            "spatialLayerColormap": {
                "A": None,
                "B": None
            },
            "featureValueColormap": {
                "A": "plasma",
                "B": "plasma"
            },
            "featureValueColormapRange": {
                "A": [
                    0,
                    1.0
                ],
                "B": [
                    0,
                    1.0
                ]
            },
            "metaCoordinationScopes": {
                "A": {
                    "spatialTargetZ": "A",
                    "spatialTargetT": "A",
                    "obsType": "A",
                    "imageLayer": "A",
                    "spotLayer": "A",
                    "obsColorEncoding": "A",
                    "featureSelection": "A"
                },
                "B": {
                    "spatialTargetZ": "A",
                    "spatialTargetT": "A",
                    "obsType": "A",
                    "imageLayer": "B",
                    "spotLayer": "B",
                    "obsColorEncoding": "B",
                    "featureSelection": "B"
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
                        "spatialLayerColormap": {
                            "A": "A"
                        },
                        "imageChannel": {
                            "A": [
                                "A"
                            ]
                        }
                    },
                    "spotLayer": {
                        "spatialLayerOpacity": {
                            "A": "B"
                        },
                        "spatialLayerVisible": {
                            "A": "B"
                        },
                        "spatialLayerColor": {
                            "A": "A"
                        },
                        "obsColorEncoding": {
                            "A": "A"
                        },
                        "spatialSpotRadius": {
                            "A": "A"
                        }
                    },
                    "imageChannel": {
                        "spatialTargetC": {
                            "A": "A",
                            "B": "B",
                            "C": "C",
                            "D": "D"
                        },
                        "spatialChannelColor": {
                            "A": "A",
                            "B": "B",
                            "C": "C",
                            "D": "D"
                        },
                        "spatialChannelWindow": {
                            "A": "A",
                            "B": "B",
                            "C": "C",
                            "D": "D"
                        },
                        "spatialChannelVisible": {
                            "A": "A",
                            "B": "B",
                            "C": "C",
                            "D": "D"
                        },
                        "spatialChannelOpacity": {
                            "A": "A",
                            "B": "B",
                            "C": "C",
                            "D": "D"
                        }
                    }
                },
                "B": {
                    "imageLayer": {
                        "fileUid": {
                            "B": "B"
                        },
                        "spatialLayerOpacity": {
                            "B": "C"
                        },
                        "spatialLayerVisible": {
                            "B": "C"
                        },
                        "photometricInterpretation": {
                            "B": "B"
                        },
                        "spatialLayerColormap": {
                            "B": "B"
                        },
                        "imageChannel": {
                            "B": [
                                "B"
                            ]
                        }
                    },
                    "spotLayer": {
                        "spatialLayerOpacity": {
                            "B": "D"
                        },
                        "spatialLayerVisible": {
                            "B": "D"
                        },
                        "spatialLayerColor": {
                            "B": "B"
                        },
                        "obsColorEncoding": {
                            "B": "B"
                        },
                        "spatialSpotRadius": {
                            "B": "B"
                        }
                    },
                    "imageChannel": {
                        "spatialTargetC": {
                            "E": "E",
                            "F": "F",
                            "G": "G",
                            "H": "H"
                        },
                        "spatialChannelColor": {
                            "E": "E",
                            "F": "F",
                            "G": "G",
                            "H": "H"
                        },
                        "spatialChannelWindow": {
                            "E": "E",
                            "F": "F",
                            "G": "G",
                            "H": "H"
                        },
                        "spatialChannelVisible": {
                            "E": "E",
                            "F": "F",
                            "G": "G",
                            "H": "H"
                        },
                        "spatialChannelOpacity": {
                            "E": "E",
                            "F": "F",
                            "G": "G",
                            "H": "H"
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
                "w": 4,
                "h": 6
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
                "x": 0,
                "y": 6,
                "w": 4,
                "h": 3
            },
            {
                "component": "spatialBeta",
                "coordinationScopes": {
                    "dataset": "A",
                    "metaCoordinationScopes": [
                        "B"
                    ],
                    "metaCoordinationScopesBy": [
                        "B"
                    ]
                },
                "x": 4,
                "y": 0,
                "w": 4,
                "h": 6
            },
            {
                "component": "layerControllerBeta",
                "coordinationScopes": {
                    "dataset": "A",
                    "metaCoordinationScopes": [
                        "B"
                    ],
                    "metaCoordinationScopesBy": [
                        "B"
                    ]
                },
                "x": 4,
                "y": 6,
                "w": 4,
                "h": 3
            },
            {
                "component": "heatmap",
                "coordinationScopes": {
                    "dataset": "A",
                    "featureSelection": "B"
                },
                "x": 0,
                "y": 9,
                "w": 8,
                "h": 3
            },
            {
                "component": "obsSetSizes",
                "coordinationScopes": {
                    "obsType": "A",
                    "dataset": "A"
                },
                "x": 8,
                "y": 0,
                "w": 2,
                "h": 6
            },
            {
                "component": "featureList",
                "coordinationScopes": {
                    "dataset": "A",
                    "featureSelection": "B"
                },
                "x": 10,
                "y": 0,
                "w": 2,
                "h": 6
            },
            {
                "component": "obsSetFeatureValueDistribution",
                "coordinationScopes": {
                    "dataset": "A",
                    "featureSelection": "B"
                },
                "x": 8,
                "y": 6,
                "w": 4,
                "h": 6
            }
        ],
        "initStrategy": "auto"
    }


if __name__ == "__main__":
    # Read in the spatialdata.kwargs.json file
    with open("spatialdata.kwargs.json", "r") as f:
        vt_kwargs = json.load(f)

    # Configure the viewer
    vt_config = format_vitessce(**vt_kwargs)

    # Save the configuration to JSON
    with open("spatialdata.vt.json", "w") as f:
        json.dump(vt_config, f, indent=4)

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
    zarr_fp: str,
    image_key: str,
    channel_names: list,
    mask_channels: list,
    schema_version = "1.0.16",
    obs_type = "cell",
    **kwargs
):
    name = "StarDist Segmentation"
    description = "Image display with cell outlines from StarDist"
    
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


def format_vitessce_cell_measurements(
    zarr_fp: str,
    image_key: str,
    obs_set_paths: List[str],
    obs_set_names: List[str],
    init_gene: str,
    schema_version = "1.0.16",
    obs_type = "cell",
    feature_type = "marker",
    spots_key = "centroids",
    feature_value_type = "expression",
    radius = 10,
    **kwargs
):
    name = "Cell Measurements"
    description = "Image display with average channel intensity for each cell"

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
                                    for path, name in zip(
                                        obs_set_paths,
                                        obs_set_names
                                    )
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
                    "A": [
                        init_gene
                    ],
                    "B": [
                        init_gene
                    ]
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
                    "A": 0,
                    "B": 0,
                },
                "spatialChannelColor": {
                    "A": [255, 255, 255],
                    "B": [255, 255, 255]
                },
                "spatialChannelWindow": {
                    "A": None,
                    "B": None
                },
                "spatialChannelVisible": {
                    "A": True,
                    "B": True
                },
                "spatialChannelOpacity": {
                    "A": 1,
                    "B": 1
                },
                "spotLayer": {
                    "A": "__dummy__",
                    "B": "__dummy__"
                },
                "spatialSpotRadius": {
                    "A": radius,
                    "B": radius
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
                                "A": "A"
                            },
                            "spatialChannelColor": {
                                "A": "A"
                            },
                            "spatialChannelWindow": {
                                "A": "A"
                            },
                            "spatialChannelVisible": {
                                "A": "A"
                            },
                            "spatialChannelOpacity": {
                                "A": "A"
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
                                "B": "B"
                            },
                            "spatialChannelColor": {
                                "B": "B"
                            },
                            "spatialChannelWindow": {
                                "B": "B"
                            },
                            "spatialChannelVisible": {
                                "B": "B"
                            },
                            "spatialChannelOpacity": {
                                "B": "B"
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


def main():
    # Read in the spatialdata.kwargs.json file
    with open("spatialdata.kwargs.json", "r") as f:
        vt_kwargs = json.load(f)

    # Configure the viewer twice, once to show segmentation
    # and a second time to show cell measurements
    for prefix, vt_config in [
        ("segmentation", format_vitessce_segmentation(**vt_kwargs)),
        ("cell_measurements", format_vitessce_cell_measurements(**vt_kwargs))
    ]:
        # Save the configuration to JSON
        with open(f"{prefix}.vt.json", "w") as f:
            json.dump(vt_config, f, indent=4)


main()
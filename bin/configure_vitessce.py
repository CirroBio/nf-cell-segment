#!/usr/bin/env python3

import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def format_vitessce(
    schema_version = "1.0.16",
    name="StarDist Processed Image",
    zarr_fp="spatialdata.zarr.zip",
    obs_set_paths=[],
    obs_set_names=[],
    init_gene="gene_a",
    channel_a=0,
    channel_b=0,
    channel_c=0,
    mask_channels={},
    rgb_a=[0, 0, 255],
    rgb_b=[0, 255, 0],
    rgb_c=[255, 0, 0],
):

    return {
        "version": schema_version,
        "name": name,
        "description": "A processed image with cell outlines and protein expression data",
        "datasets": [
            {
                "uid": "A",
                "name": name,
                "files": [
                    {
                        "url": zarr_fp,
                        "fileType": "image.spatialdata.zarr",
                        "coordinationValues": {
                            "fileUid": "image",
                            "obsType": "cell"
                        },
                        "options": {
                            "path": f'images/image'
                        }
                    },
                    {
                        "url": zarr_fp,
                        "fileType": "obsFeatureMatrix.spatialdata.zarr",
                        "coordinationValues": {
                            "obsType": "cell"
                        },
                        "options": {
                            "path": "tables/table/X"
                        }
                    },
                    {
                        "url": zarr_fp,
                        "fileType": "obsSpots.spatialdata.zarr",
                        "coordinationValues": {
                            "obsType": "cell"
                        },
                        "options": {
                            "path": "shapes/cells",
                            "tablePath": "tables/table"
                        }
                    },
                    {
                        "url": zarr_fp,
                        "fileType": "obsSets.spatialdata.zarr",
                        "coordinationValues": {
                            "obsType": "cell"
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
                "A": "cell"
            },
            "featureType": {
                "A": "marker"
            },
            "featureValueType": {
                "A": "expression"
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
                "A": "image",
                "B": "image"
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
                "A": channel_a,
                "B": channel_b,
                "C": channel_c,
                "D": mask_channels["cell"],
                "E": mask_channels["nucleus"],
                "F": 0
            },
            "spatialChannelColor": {
                "A": rgb_a,
                "B": rgb_b,
                "C": rgb_c,
                "D": [255, 165, 0],
                "E": [255, 255, 255],
                "F": [255, 0, 0]
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


if __name__ == "__main__":
    # Read in the spatialdata.kwargs.json file
    with open("spatialdata.kwargs.json", "r") as f:
        vt_kwargs = json.load(f)

    # Configure the viewer
    vt_config = format_vitessce(**vt_kwargs)

    # Save the configuration to JSON
    with open("spatialdata.vt.json", "w") as f:
        json.dump(vt_config, f, indent=4)

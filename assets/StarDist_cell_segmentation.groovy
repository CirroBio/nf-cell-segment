import qupath.lib.gui.tools.MeasurementExporter
import qupath.lib.objects.PathCellObject
import qupath.ext.stardist.StarDist2D
import java.awt.image.BufferedImage
import qupath.lib.images.servers.ImageServerProvider
import qupath.opencv.ops.ImageOps

def threshold = args[5] as float
def pixelSize = args[6] as float
def channels = args[7] as int
def cellExpansion = args[8] as int
def cellConstrainScale = args[9] as float

def stardist = StarDist2D
        .builder(args[0])
        .threshold(threshold)        // Probability (detection) threshold
        .preprocess(
                ImageOps.Core.subtract(100),
                ImageOps.Core.divide(100)
        )
        .pixelSize(pixelSize)        // Resolution for detection
        .channels(channels)                 // Select detection channel
        .cellExpansion(cellExpansion)          // Approximate cells based upon nucleus expansion
        .cellConstrainScale(cellConstrainScale)     // Constrain cell expansion using nucleus size
        .measureShape()              // Add shape measurements
        .measureIntensity()          // Add cell measurements (in all compartments)
        .includeProbability(true)    // Add probability as a measurement (enables later filtering)
        .build()

def projectDir = new File(args[2])
def project = Projects.createProject(projectDir , BufferedImage.class)
def inputFile = new File(args[3])
def server = new qupath.lib.images.servers.bioformats.BioFormatsServerBuilder().buildServer(inputFile.toURI())
def imageData = new ImageData(server)
def entry = project.addImage(server.getBuilder())
entry.setImageName(server.getMetadata().getName())
entry.setThumbnail(qupath.lib.gui.commands.ProjectCommands.getThumbnailRGB(server))

entry.saveImageData(imageData)
project.syncChanges()
def pathObjects = createFullImageAnnotation(imageData, true)

stardist.detectObjects(imageData, pathObjects, true)
entry.saveImageData(imageData)
project.syncChanges()

// Get the list of all images in the current project
def imagesToExport = project.getImageList()
def separator = ","

// Choose the columns that will be included in the export
// Note: if 'columnsToInclude' is empty, all columns will be included
def columnsToInclude = new String[]{}

// Choose the type of objects that the export will process
// Other possibilities include:
//    1. PathAnnotationObject
//    2. PathDetectionObject
//    3. PathRootObject
// Note: import statements should then be modified accordingly
def exportType = PathCellObject.class

// Choose your *full* output path
def outputFile = new File(args[1])

// Create the measurementExporter and start the export
println 'Exporting measurements'
def exporter  = new MeasurementExporter()
                  .imageList(imagesToExport)            // Images from which measurements will be exported
                  .separator(separator)                 // Character that separates values
                  .exportType(exportType)               // Type of objects to export
                  .includeOnlyColumns(columnsToInclude) // Columns are case-sensitive
                  .exportMeasurements(outputFile)        // Start the export process

// Export the cell shapes as GeoJSON
println 'Exporting cell shapes'

def annotations = imageData.getHierarchy().getCellObjects()
def geoJsonPath = args[4]
exportObjectsToGeoJson(annotations, geoJsonPath)

println 'Done!'
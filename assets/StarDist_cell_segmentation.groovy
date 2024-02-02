import qupath.lib.gui.tools.MeasurementExporter
import qupath.lib.objects.PathCellObject
import qupath.ext.stardist.StarDist2D
import java.awt.image.BufferedImage
import qupath.lib.images.servers.ImageServerProvider

def stardist = StarDist2D
        .builder(args[0])
        .threshold(0.5)              // Probability (detection) threshold
        .normalizePercentiles(1, 99) // Percentile normalization
        .pixelSize(0.50)             // Resolution for detection
        .channels(0)                 // Select detection channel
        .cellExpansion(5.0)          // Approximate cells based upon nucleus expansion
        .cellConstrainScale(1.5)     // Constrain cell expansion using nucleus size
        .measureShape()              // Add shape measurements
        .measureIntensity()          // Add cell measurements (in all compartments)
        .includeProbability(true)    // Add probability as a measurement (enables later filtering)
        .build()

def projectDir = new File(args[2])
def project = Projects.createProject(projectDir , BufferedImage.class)
def inputFile = new File(args[3])
def server = new qupath.lib.images.servers.bioformats.BioFormatsServerBuilder().buildServer(inputFile.toURI())
def imageData = new ImageData(server)
// def imageData = getCurrentImageData(server2)
// def server = imageData.getServer()
def entry = project.addImage(server.getBuilder())
entry.setImageName(server.getMetadata().getName())
entry.setThumbnail(qupath.lib.gui.commands.ProjectCommands.getThumbnailRGB(server))

entry.saveImageData(imageData)
project.syncChanges()
// def pathObjects = getSelectedObjects()
def pathObjects = createFullImageAnnotation(imageData, true)

stardist.detectObjects(imageData, pathObjects, true)
entry.saveImageData(imageData)
project.syncChanges()

// Get the list of all images in the current project
// // def project = getProject()
def imagesToExport = project.getImageList()
// def imagesToExport = [project.getEntry(getCurrentImageData())]
def separator = ","

// // Choose the columns that will be included in the export
// // Note: if 'columnsToInclude' is empty, all columns will be included
// def columnsToInclude = new String[]{"Name", "Class", "Nucleus: Area"}
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
def exporter  = new MeasurementExporter()
                  .imageList(imagesToExport)            // Images from which measurements will be exported
                  .separator(separator)                 // Character that separates values
                  .exportType(exportType)               // Type of objects to export
                  .includeOnlyColumns(columnsToInclude) // Columns are case-sensitive
                  .exportMeasurements(outputFile)        // Start the export process
                //   .filter(obj -> obj.getPathClass() == getPathClass("Tumor"))    // Keep only objects with class 'Tumor'

println 'Done!'
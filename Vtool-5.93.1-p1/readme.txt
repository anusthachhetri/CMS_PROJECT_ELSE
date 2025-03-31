----------------------------------------------------------------------------------------
-------------------------------------Vtool----------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
Vtool (version 5.93.1)
-----------------------------------------------------------------------
The Vtool developers wish to acknowledge the use of the following software:

 1. Saxon XSLT and XQuery Processor from Saxonica Limited (see http://www.saxonica.com/)
 2. PDFBox and FontBox (see http://pdfbox.apache.org/licenses/license-2.0)
 3. Sanselan, MimeUtil and Resolver (see http://www.fightingquaker.com/sanselan/, http://www.apache.org/licenses/) 
 4. Epubcheck project (see http://code.google.com/p/epubcheck/)
 5. JENA - A Semantic Web Framework for Java (see http://jena.sourceforge.net/index.html)
 6. json-schema-validator - A java framework for validating JSON against JSON Schema (see https://github.com/fge/json-schema-validator)
 7. json-path - A java framework for searching JSON path in JSON (see https://github.com/jayway/JsonPath)
 8. snakeyaml - YAML parser and emitter for JAVA programming language (see https://code.google.com/p/snakeyaml/)
 9. SHACL library- To validate datagraph against shape graph (see https://github.com/TopQuadrant/shacl)
10. Media library - To extract informations from media (video and audio) files (see http://jcodec.org)
----------------------------------------------------------------------------------------
 Instructions for installing and running this Vtool:
----------------------------------------------------------------------------------------

1) For Vtool to work, Open JDK 1.8.0 or higher should be installed in your system, which can be downloaded from https://adoptopenjdk.net/releases.html?variant=openjdk8&jvmVariant=hotspot
2) To install Vtool:

------------
 Method 1
------------

 Windows: Extract Vtool-5.93.1-Install.exe from Vtool-5.93.1-Install.zip and double-click on Vtool-5.93.1-Install.exe to install the  Vtool.  The installation defaults to C:\Program Files\Elsevier\Vtool\. The  location can be changed in the installer program.

 Unix: Unzip all the contents of the Vtool-5.93.1.zip to any installation folder of your choice. To link the startup shell script to /usr/bin/vtool, run Vtool-5.93.1-Install.sh. You need superuser privilege or you can use "sudo Vtool-5.93.1-Install.sh".

 If JRE is not installed on your computer, you will be directed to download it. If JAVA 1.8 is available in your system as a portable JDK/JVM (downloaded from the URL: <a href="https://adoptopenjdk.net/releases.html?variant=openjdk8&jvmVariant=hotspot">https://adoptopenjdk.net/releases.html?variant=openjdk8&jvmVariant=hotspot</a>), you have to set the environment "PATH" variable. It is also possible to run this portable JAVA without setting the path in environment variable. During, installation, if JAVA path is not set, VTool will assume that JAVA is not available and prompt to install JAVA. It also has the option to continue VTool installation, if you have a portable JAVA available in your system

------------
 Method 2
------------

 Extract the entire contents of Vtool-5.93.1.zip to a convenient folder.

3) To run Vtool:

  Open Command Window (or a Terminal in Linux)

  Run the Vtool in the command-line as follows:
  
If you have used Method 1 for installing Vtool, use  

vtool [options] [-log stdout|filename] -file inputfile


If you have used Method 2 for installing Vtool, use

java -Xmx1024m -jar vtool.jar [options] [-log stdout|filename] -file inputfile


Either the full path or the relative path can be provided as inputs.

If you have used Method 2, then for Vtool to work, you will have to set the system environment variable for the Vtool (VTOOL_DIR) which can be called from the vtool.bat or vtool.sh.

Vtool may require up to 1024MB virtual memory for handling images. If  you have used Method 1 to install Vtool, the maximum Java heap  size is set automatically. Otherwise, use java -Xmx1024m to indicate the maximum required Java heap size to the JVM. If an XML file had more than 64,000 entities, SAXParseException will be thrown by the Vtool. This exception can be avoided by adding -DentityExpansionLimit=200000 (which will increase the entity expansion limit) to the java command line option.

java -Xmx1024m -DentityExpansionLimit=200000 -jar vtool.jar [options] [-log stdout|filename] -file inputfile


 Vtool options include:


	-version               	Show the version number.
	-specver               	Show the version of the spec file.	
	-file filename         	The name of the file or directory to check (�file is optional if no other options are specified; filename should be enclosed
							within quotes if it contains white space). If the input is directory, files and subdirectories in the directory are processed. If there is dataset.xml in directory, the corresponding subdirectories to dataset.xml are made to run as dataset. The excluded files and directories are treated as individual process and are made to run. Directory option will check till the last file of last subdirectory in the folder hierarchy. 						   
	-help   	            Show usage and exit
	-time      	            Display the time taken by this application.
	-forcecheck            	This forces Vtool to do the entire validation even if the input file has not been changed since the last run.
	-nofp                   This option is used to automatically delete the fingerprint file.
	-log filename          	Specify the log file.
	-withlinking           	Validate cross-references in book datasets.
	-skip \"id1 id2...\"   	Skip checks by check id.
	-skipbypii 		 		\"PII:pii1 id11 id12 ... PII:pii2 id21 id22 ... \"
								Skip checks by PII and check id. (Note: input file should have a unique PII; PII without parentheses, hyphens, or spaces should be specified).
	-lite	        		This option is used to validate the XML as a �Head-only� or �Head-and-Tail� file.
	-spawn          		Validate graphics files and stripins.
							This option need not be specified if the input file is a dataset.xml.
							It needs to be specified only when the input is a main.xml and you want a fingerprint created for the associated graphics files and stripins also (Note: folder structure should follow the CONTRAST standard for -spawn to work).
	-stripin	    		Validate strip-in images for dataset, individual XML with stripin images(Note: folder structure should follow the
							CONTRAST standard for -stripin to work) and individual stripin image files.
	-bph       	    		Validate file as a batch-placeholder
	-no-xmp		   			Skip XMP checks for a PDF file of Elsevier PDF version 5.2 or less 
							(Note:  (i) this	option should  be used only when the input is an individual PDF file. 
									(ii) this option need not be used when the input is dataset.xml)
	-book-metadata  		Validate the cover image of an O300 dataset 
							(Note:    (i) this option should be used only when the input file is a cover image. 
									  (ii) this option need not be used when the input is dataset.xml) 	  
	-EWXOCS         		This option is used to validate checks on journal or book output datasets.
	-noimg		    		This option is used to skip image checks on journal or book output datasets. 
							This will work only when -EWXOCS option is used and for output datasets only.
	-mrw		    		This option is used to validate MRW checks on Book 5.3.0 DTD and higher datasets with docsubtype "com" or "enc".
	-satellite				This option should be used only when the input is an individual satellite RDF XML file.
	-xhtml					This option should be used only when the input is an individual XHTML file.
	-patentf				This option is used to support the Opsbank Excerption workflow checks on CAR files.
 	-rdf					This option is used to validate RDF XML files to detect RDF errors using JENA Application, a Semantic Webframework.
	-v						This option is used to validate very large XML files
	-vcclog					This option is used to give the vcclog XML path as input to pharmapendium.
    -schematron [filename]  This option is used to invoke schematron process, optional *.sch file or directory. 
	-nofpdtd				This option is used to keep the fingerprint file as external DTD.
    -vjson [schemaName]         		This option is used to invoke the JSON validation. JSON schema name can be given as an  optional value to validate the input json against the defined schema
                                                vjson with JSON schema name as value, then consider the JSON schema and performs VTW payload  validation 
                                                vjson with keyword "grant", will start assessing the type of grant and initiate the Grant payload validation                                                      
    -am                         This option should be used only when the input is an individual PDF file.
    -ap-pf                      This option is used to validate json for Apollo preflight.
    -ap-as <manifest JSON>      This option is used to validate xml for Apollo AutoStructure (S5 XML) and must contain manifest JSON path.
    -ap-pc <Item XML>      This option is used to validate pdf for Apollo PageComposition(S5 PDF) and must contain item XML file path.
    -ap-aa [-gaimage]      This option is used to validate image for Apollo AssessAndNormalizeArtwork, optional gaimage.
           <-assettype>    The switch is mandatory. 
    -ap-tp <manifest JSON>      This option is used to validate xml for Apollo InteractiveCopyEditing(S100 XML) and must contain manifest JSON path.
    -ap-ap [-gaimage]      This option is used to validate image for Apollo CreatePrintArtwork, optional gaimage.
           <-assettype>    The switch is mandatory.
    -gaimage <ISSN or JID> This option is used to validate Graphical Abstract Image for Apollo Service and must contains ISSN or JID value.	
    -ap-cp <Item XML>       This option is used to validate pdf for Apollo ComposePDF and must contain item XML file path
            <-assettype>    The switch is mandatory, item XML can be given as input for Web PDF files.
            [manifest JSON] The switch can have a manifest JSON path as optional.    
    -ap-cs                  This option is used to validate pdf for Apollo ComposeSemiFinishedPDF.
             <-assettype>   The switch is mandatory, item XML can be given as input for Web PDF files.     
    -ap-st <Item XML>      This option is used to validate pdf for Apollo StampPDF and must contain item XML file path 
            <-assettype>    The switch is mandatory, item XML can be given as input for Web PDF files.   
 	   [manifest JSON] The switch can have a manifest JSON path as optional.
 	-ap-md                 This option is used to validate for Apollo Merged PDF.
    -ap-nn [-gaimage]      This option is used to validate for Non-CPC, Artwork, non-CAP files, optional gaimage.
           <-assettype>    The switch is mandatory.
    -ap-np                 This option is used to validate Web and Print PDF files for Non-CPC files.
          <-assettype>     The switch is mandatory, item XML can be given as input for Web PDF files.
    -ap-cpc                This option is used to validate XML files and their CAP assets for CPC. 
    -pts                   PTS Order XML file.
    -vgraph                To use the validation-graph created by VTool during payload JSON validation (vtl-mnf json path or value "no" is allowed).
    -shacl <shapegraph>    This option is used to validate datagraph against shapegraph.
    -servicecall <JSON>    This option is used to retrieve the stage, JSON File is mandatory.
    -led                   This option is used to validate HTML5+LED document inputs.
    -gba                   This option is used to validate Global Book Archive deliverables, S300 'dataset.xml' path must be given as input.
    -cct                   This option is used to validate CCT (Commissioned Content Translation) project deliverables.
    -submres               This option is used to supply supporting manuscript assets from submission platform.
    -cpld	               This option is used to validate the CP/LD assets.
-----------------------------------------------------------------------------
Refer to the Vtool user guide for further details including deprecated options.
-----------------------------------------------------------------------------

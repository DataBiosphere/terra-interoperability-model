## Terra Interoperability Model

### What is the Terra Interoperability Model (TIM)?
TIM is a data model that captures a common set of concepts and relationships for biomedical research intended to facilitate and encourage data sharing and reuse.  Its purpose is to enable researchers to find highly connected biomedical data in a federated search space and support interoperability among datasets.  

Examples of searches include:

* *Find all glioma data that I can access for commercial research*
* *Find single-cell data from samples with HIV and an intracellular pathogen*
* *I need RNA-seq, Hi-C, and ChIP-seq data from adult brain tissue -- normal and diseased with malignant glioma*

TIM is formally specified using OWL and is currently available in the [Turtle](https://www.w3.org/TR/turtle/) RDF serialization format.  It is expected that the data model will be translated into appropriate syntaxes for implementation across a range of applications.  See [Using Terra Interoperability Model](#using-Terra-Interoperability-Model).  The namespace and default prefix are "TerraCore".

The data model has been developed by The Broad Institute of MIT and Harvard’s Data Science Platform team and the Core Data Model Team at the Broad.  Our intent is to open this model to the biomedical community for improvement over time while ensuring it remains a minimal model supporting search and analysis for researchers.  

### Terminology: Data Model, Ontology, Knowledge Graph, Schema
These terms are often used interchangeably<sup>1</sup>.  We use them as follows.
* An **ontology** is a formally specified vocabulary which defines the concepts and relationships that characterize a domain.  Further, we assume that an ontology represents all key high-level concepts in a domain and minimally provides parent-child relationships among the concepts.
* A **data model** connects various domain vocabularies to “connect the dots” with a specific purpose in mind.  It is intended to capture how the data are connected in ways that are meaningful to subject matter experts.  Data models are specific to selected use cases or objectives.  A good data model leverages standard vocabularies often in the form of ontologies and defines and extends concepts and relationships only when necessary. One can view a data model as a reusable design for one or more schemas.<sup>2</sup>
* A **knowledge graph** is a data model graph implementation populated with data.
* A **schema** defines the structure generally used to store data. It is often an implementation of a data model either implicitly or explicitly but usually includes optimizations for storage or performance that are not relevant to the data model. Examples of schemas include [HCA's JSON schemas](https://github.com/HumanCellAtlas/metadata-schema/tree/master/json_schema), a  Postgres or MySQL schema, or a schema for Google's BigQuery.  

### Illustration
The following diagram illustrates selected key concepts and relationships to provide an overview of the model.  It is produced using [Cmap](https://cmap.ihmc.us/) from the Florida Institute for Human & Machine Cognition (IHMC).<br>

Prefixes are shorthand to reference concepts and properties in another namespace.  The following prefixes are used in the illustration.

* Default PREFIX : <https://datamodel.terra.bio/TerraCore#> .  
* PREFIX core: represents one of the 3 Terra Interoperability Model Core models
  * <https://datamodel.terra.bio/TerraCore#> .
  * <https://datamodel.terra.bio/TerraCoreValueSets#> .
  * <https://datamodel.terra.bio/TerraDCAT_ap#> .
* PREFIX dcat: <http://www.w3.org/ns/dcat#> .
* PREFIX duo: <http://purl.obolibrary.org/obo/duo-basic.owl#> .<br>
* PREFIX obo: <http://purl.obolibrary.org/obo/> .<br>
* PREFIX prov: <http://www.w3.org/ns/prov#> .<br>
* PREFIX skos: <http://www.w3.org/2004/02/skos/core#> .

![Figure - Terra Interoperability Model Overview Draft](https://github.com/DataBiosphere/terra-interoperability-model/blob/master/documents/Terra%20Interoperability%20Model%20V1.jpg)

### Status
The Terra Interoperability Model is currently under development, is available in Turtle (.ttl) serialization form, and may be released in other forms over time.

### Versions
<b>Stable Release Versions</b><br>
  Release 1.x is currently available.  Some additions are expected by end Q1 2021. At that point, we anticipate that the data model will be backwards compatible.

It is our intention to begin designating specific classes as "stable" as the model develops and to offer Stable Release Versions as the model matures.

### How Did Terra Interoperability Model Come About?

Since its founding, the Broad Institute has been involved in systematic efforts to create large datasets to serve as a foundation for biological and medical studies around the world.  These efforts require collecting data and their provenance, but also enabling researchers to find and reuse the data.  How do we do this as the volume, variety, and complexity of biomedical data increases?  At a minimum, we need to understand the data and how they are connected.  

Historically most biomedical data have been collected in silos as a side effect of source, project structure, research purpose, data type, funding, etc.  Through the Internet and cloud storage we increasingly have access to these massive datasets. 

The Broad Institute is committed to sharing data and knowledge. In defining data models, we aspire to the principles of the Data BioSphere<sup>3</sup> and the FAIR<sup>4</sup> guiding principles, notably:
* Open, community-driven, and standards-based data models
* Findable, accessible, interoperable, and reusable data

A number of national and international efforts have influenced our thinking in developing this data model.  To name only a few, we began by reviewing data models from Genomic Data Commons, Human Cell Atlas, NCBI Biosamples, and EMBL-EBI BioSamples.  (Please see Acknowledgements for a more complete list.)  When reviewing data models we found some focus on a particular subdomain, capturing more detail than we needed, while others are developed to address a different need.  We found that we were missing a cross-domain data model that could allow us to focus on our needs around finding and analyzing data.  

We then formed a team of researchers from across the Broad Institute to ensure that the data model is consistent with the science.  If we follow the science, our data model will more accurately reflect the domain and enable researchers to find data using what are, for them, natural connections.  We recognize that we will need to create new relationships and add data points as time and science progress. 

Finally, we selected several datasets to test the model in our own pilot project.

### Using Terra Interoperability Model
TIM is currently composed of three separate OWL/TTL files. TerraDCAT_ap.ttl is an extension of the (W3C's Data Catalog Vocabulary)[https://www.w3.org/TR/vocab-dcat-2/] which adds data use terms from the (Data Use Ontology)[https://github.com/EBISPOT/DUO].  TerraCoreValueSets.ttl provides controlled vocabulary terms to support TerraCoreDataModel.ttl which contains the classes and properties required to connect core biomedical data concepts.

The list of external ontologies and vocabularies that are used in the Terra Interoperability Model can be found in the [Ontologies document](documents/Ontologies.md).

In addition to the formal specification in OWL (serialized in Turtle format), the Data Sciences Platform Team has defined a JSON representation of the Data Model that will be used internally at Broad Institute to pilot the data model.  This JSON representation will be ingested into the Terra Repository and implemented using Google's BigQuery.  This is an example of how the data model can be used to design schemas.  

### License
[BSD 3-Clause License](https://github.com/DataBiosphere/terra-interoperability-model/blob/master/LICENSE)

### Contact
Please use this repository's [Issue Tracker](https://github.com/broadinstitute/dsp-data-models/issues "Issue Tracker") to share comments or concerns related to the data model.  TIM is not currently open to public contribution; it is currently wholly managed by Broad’s DSP Data Modeling Team.

### Acknowledgements
**Data Sciences Platform, Broad Institute**  

Dan Moran, Sarah Wessel, Jeremy Hert, Raaid Arshad, Quazi Hoque, Rori Cremer, Andrea Haessly, Jeff Korte, Jerome Chadel, David Wine, and others.

**Terra Core Data Model Team, Broad Institute**  
Larry Babb, Senior Principal Software Engineer  
Paul Clemons, PhD, Director, Computational Chemical Biology Research
Sid Cox, PhD, Senior Data Modeler
Rachel Liao, PhD, Scientific Advisor to the Director
Eugenio Mattei, PhD, Computational Scientist
Marco Ocana, Principal Software Engineer   
Kathy Reinold (Chairperson), Principal Data Modeler  
Noam Shoresh, PhD, Associate Director, Computational Biology, Epigenomics Program    
Kathleen Tibbetts, Director, Data Engineering, Data Sciences Platform  
Timothy Tickle, PhD, Principal Product Manager
Kyle Vernest, Head of Project Management, Data Sciences Platform
Andrew Zimmer, Director, Data Donation Platform

**Guest Subject Matter Experts**

Charles Epstein
Orr Ashenberg
Tommaso Biancalani
Caroline Porter

**Alumni Contributors**

Clare Bernard, PhD, Senior Director of Product, Data Science Platform  
Sinéad Chapman, Associate Director, Genetics Project Management, Stanley Center for Psychiatric Research  

We are also grateful for the work of many other groups who have contributed through prior and ongoing work in this area.  Several groups have graciously allowed us to participate in standards discussions, such as the Human Cell Atlas Metadata Community, NCI's [Center for Cancer Data Harmonization](https://datascience.cancer.gov/data-commons/center-cancer-data-harmonization-ccdh), [Single Cell Portal](https://portals.broadinstitute.org/single_cell "Single Cell Portal") and several [GA4GH Working Streams](https://www.ga4gh.org/how-we-work/workstreams "GA4GH Working Streams").

**Alumni Contributors, Broad Institute**<br>
Ben Carlin

**Data models:** [Genomic Data Commons](https://gdc.cancer.gov/developers/gdc-data-model/gdc-data-model-components "Genomic Data Commons"), [BioCompute](https://github.com/biocompute-objects/BCO_Specification "BioCompute"), [Human Cell Atlas Metadata](https://data.humancellatlas.org/metadata "Human Cell Atlas Metadata"), [EMBL-EBI BioSamples](https://www.ebi.ac.uk/biosamples/docs/references/sampletab "EMBL-EBI BioSamples"), [Bioschemas](https://bioschemas.org/specifications/ "Bioschemas"), [Encode](https://www.encodeproject.org/profiles/ "Encode"), [NCBI Biosamples](https://submit.ncbi.nlm.nih.gov/biosample/template/?package=Human.1.0&action=definition "NCBI Biosamples").

**Ontology/Vocabulary sources:** [W3C](https://www.w3.org/ "W3C") ([DCAT](https://w3c.github.io/dxwg/dcat/ "DCAT"), [PROV-O](https://www.w3.org/TR/prov-o/ "PROV-O")), [OBO Foundry,](http://obofoundry.org/ "OBO Foundry,") [EMBL-EBI’s Ontology Lookup Service](https://bioportal.bioontology.org/ontologies "EMBL-EBI’s Ontology Lookup Service"), [BioPortal](https://bioportal.bioontology.org/ontologies "BioPortal")

### References

<sup>1</sup>https://www.w3.org/standards/semanticweb/ontology 

<sup>2</sup>https://www.w3.org/TR/dwbp/#dataVocabularies

<sup>3</sup>https://medium.com/@benedictpaten/a-data-biosphere-for-biomedical-research-d212bbfae95d

<sup>4</sup>https://www.nature.com/articles/sdata201618

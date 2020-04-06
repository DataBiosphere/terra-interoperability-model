## Core Data Model for Terra (Terra Core)

### What is Terra Core?
The Core Data Model for Terra is a common data model for biomedical research intended to facilitate and encourage data sharing and reuse.  Its purpose is to enable researchers to find highly connected biomedical data in a federated search space.  

Examples of searches include:
* *Find all glioma data that I can access for commercial research*
* *Find single-cell data from samples with HIV and an intracellular pathogens*
* *I need RNA-seq, Hi-C, and ChIP-seq data from adult brain tissue -- normal and diseased - with malignant glioma*

The Core Data Model for Terra is formally specified using OWL and is currently available in the [Turtle](https://www.w3.org/TR/turtle/) RDF serialization format.  It is expected that the data model will be translated into appropriate syntaxes for implementation across a range of applications.  See [Using Terra Core](#using-Terra-Core).  The namespace and default prefix are "TerraCore".

The data model has been developed by The Broad Institute of MIT and Harvard’s Data Science Platform team and the Terra Core Data Model Team at the Broad.  Our intent is to open this to the biomedical community for improvement over time while ensuring it remains a minimal model supporting search and analysis for researchers.  

### Terminology: Data Model, Ontology, Knowledge Graph, Schema
These terms are often used interchangeably<sup>1</sup>.  We use them as follows.
* An **ontology** is a formally specified vocabulary which defines the concepts and relationships that characterize a domain.  Further, we assume that an ontology represents all key high-level concepts in a domain and minimally provides parent-child relationships among the concepts.
* A **data model** connects various domain vocabularies to “connect the dots” with a specific purpose in mind.  It is intended to capture how the data is connected in ways that are meaningful to subject matter experts.  Data models are specific to selected use cases or objectives.  A good data model leverages standard vocabularies often in the form of ontologies and defines and extends concepts and relationships only when necessary.<sup>2</sup>
* A **knowledge graph** is a data model populated with data.
* A **schema** defines the structure of the data generally used to store data. It is often an implementation of a data model either implicitly or explicitly but usually includes optimizations for storage or performance that are not relevant to the data model. Examples of schemas include the relational schemas used for a particular dataset in Google's BigQuery or other relational database systems, HCA's JSON schema for [Biomaterial-Cell line](https://data.humancellatlas.org/metadata/dictionary/biomaterial/cell_line).

![Figure - Terra Core Data Model Overview Draft](https://github.com/DataBiosphere/terra-core-data-model/blob/master/documents/TerraCoreDataModel-Overview_Apr2020.jpg)

### Status
The Core Data Model for Terra is currently under development, is available in Turtle (.ttl) serialization form and may be released in other forms over time.

### Versions
Stable Release Versions
Not yet available

### How Did Terra Core Come About?

Since its founding, the Broad Institute has been involved in systematic efforts to create large datasets to serve as a foundation for biological and medical studies around the world.  These efforts require collecting data and their provenance, but also enabling researchers to find and reuse the data.  How do we do this as the volume, variety, and complexity of biomedical data increases?  At a minimum, we need to understand the data and how they are connected.  

Historically most biomedical data have been collected in silos as a side effect of source, project structure, research purpose, data type, funding, etc.  Through the Internet and cloud storage we increasingly have access to these massive datasets. 

The Broad Institute is committed to sharing data and knowledge. In defining data models, we aspire to the principles of the Data BioSphere<sup>3</sup> and the FAIR<sup>4</sup> guiding principles, notably:
* Open, community-driven, and standards-based data models
* Findable, accessible, interoperable, and reusable data

A number of national and international efforts have influenced our thinking in developing this data model.  To name only a few, we began by reviewing data models from Genomic Data Commons, Human Cell Atlas, NCBI Biosamples, and EMBL-EBI BioSamples.  (Please see Acknowledgements for a more complete list.)  When reviewing data models we found some focus on a particular subdomain, capturing more detail than we needed, while others are developed to address a different need.  We found that we were missing a cross-domain data model that could allow us to focus on our needs around search and finding data.  

We then formed a team of researchers within the Broad to ensure that the data model is consistent with the science.  If we follow the science, our data model will more accurately reflect the domain and enable researchers to find data using what are, for them, natural connections.  We recognize the need to create new relationships and add data points as time and science progress. 

Finally, we selected several datasets to test the model in our own pilot project.

### Using Terra Core
Terra Core is currently composed of three separate OWL files. TerraDCAT_ap.ttl is an extension of the (W3C's Data Catalog Vocabulary)[https://www.w3.org/TR/vocab-dcat-2/] which adds data use terms from the (Data Use Ontology)[https://github.com/EBISPOT/DUO].  TerraCoreValueSets.ttl provides controlled vocabulary terms to support TerraCoreDataModel.ttl which contains the classes and properties required to connect core biomedical data concepts.

In addition to the formal specification in OWL (serialized in Turtle format), the Data Sciences Platform Team has defined a JSON representation of the Data Model that will be used internally at Broad Institute to pilot the data model.  This JSON representation will be ingested into the Terra Repository, implemented using Google's BigQuery.  This is an example of how the data model can be used to design schemas.  

### License
[BSD 3-Clause License](https://github.com/broadinstitute/dsp-data-models/blob/master/LICENSE)

### Contact
Please use this repository's [Issue Tracker](https://github.com/broadinstitute/dsp-data-models/issues "Issue Tracker") to share comments or concerns related to the data model.  Terra Core is not currently open to public contribution; it is currently wholly managed by Broad’s DSP Team.

### Acknowledgements
**Data Sciences Platform, Broad Institute**  
Dan Moran, Sarah Wessel, Jeremy Hert, Ben Carlin, Raaid Arshad, Quazi Hoque, Rori Cremer, Andrea Haessly, Jeff Korte, Emily Munro-Ludders, Jerome Chadel,David Wine, Denis Loginov, and others.

**Terra Core Data Model Team**  
Larry Babb, Senior Principal Software Engineer  
Clare Bernard, PhD, Director of Product, Data Science Platform  
Sinéad Chapman, Associate Director, Genetics Project Management, Stanley Center for Psychiatric Research  
Paul Clemons, PhD, Director, Computational Chemical Biology Research   
Rachel Liao, PhD, Scientific Advisor to the Director   
Marco Ocana, Principal Software Engineer   
Kathy Reinold, Principal Data Modeler  
Noam Shoresh, PhD, Associate Director, Computational Biology, Epigenomics Program    
Kathleen Tibbetts, Director, Data Engineering, Data Sciences Platform  
Timothy Tickle, PhD, Principal Product Manager  
Andrew Zimmer, Director, Data Donation Platform  

We are also grateful for the work of many other groups who have contributed through prior and ongoing work in this area.  Several groups have graciously allowed us to participate in standards discussions, such as the NCI Cancer Research Data Metadata group, [Single Cell Portal](https://portals.broadinstitute.org/single_cell "Single Cell Portal") and several [GA4GH Working Streams](https://www.ga4gh.org/how-we-work/workstreams "GA4GH Working Streams").

**Data models:** [Genomic Data Commons](https://gdc.cancer.gov/developers/gdc-data-model/gdc-data-model-components "Genomic Data Commons"), [BioCompute](https://github.com/biocompute-objects/BCO_Specification "BioCompute"), [Human Cell Atlas Metadata](https://data.humancellatlas.org/metadata "Human Cell Atlas Metadata"), [EMBL-EBI BioSamples](https://www.ebi.ac.uk/biosamples/docs/references/sampletab "EMBL-EBI BioSamples"), [Bioschemas](https://bioschemas.org/specifications/ "Bioschemas"), [Encode](https://www.encodeproject.org/profiles/ "Encode"), [NCBI Biosamples](https://submit.ncbi.nlm.nih.gov/biosample/template/?package=Human.1.0&action=definition "NCBI Biosamples").

**Ontology/Vocabulary sources:** [W3C](https://www.w3.org/ "W3C") ([DCAT](https://w3c.github.io/dxwg/dcat/ "DCAT"), [PROV-O](https://www.w3.org/TR/prov-o/ "PROV-O")), [OBO Foundry,](http://obofoundry.org/ "OBO Foundry,") [EMBL-EBI’s Ontology Lookup Service](https://bioportal.bioontology.org/ontologies "EMBL-EBI’s Ontology Lookup Service"), [BioPortal](https://bioportal.bioontology.org/ontologies "BioPortal")

### References

<sup>1</sup>https://www.w3.org/standards/semanticweb/ontology 

<sup>2</sup>https://www.w3.org/TR/dwbp/#dataVocabularies

<sup>3</sup>https://medium.com/@benedictpaten/a-data-biosphere-for-biomedical-research-d212bbfae95d

<sup>4</sup>https://www.nature.com/articles/sdata201618



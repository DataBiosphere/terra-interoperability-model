## DSPCore Data Model

### What is DSPCore
DSPCore is a common data model proposal for biomedical research intended to facilitate and encourage data sharing and reuse.  Its purpose is to enable researchers to find highly connected biomedical data in a federated search space.  

Examples of searches include:
* *Find all glioma data that I can access for commercial research*
* *Find single-cell data from samples with HIV and an intracellular pathogens*
* *I need RNA-seq, Hi-C, and ChIP-seq data from adult brain tissue -- normal and diseased - with malignant glioma*

The DSPCore data model is formally specified using OWL and is available in RDF serialization formats.  It is expected that the data model will be translated into appropriate syntaxes for implementation across a range of applications.  See [Using DSPCore](#using-dspcore).

The data model has been developed by The Broad Institute of MIT and Harvard’s Data Science Platform team and the DSPCore Data Model Team at the Broad.

### Terminology: Data Model, Ontology, Knowledge Graph
These terms are often used interchangeably<sup>1</sup>.  We use them as follows.
* An **ontology** is a formally specified vocabulary which defines the concepts and relationships that characterize a domain.  Further, we assume that an ontology represents all key high-level concepts in a domain and minimally provides parent-child relationships among the concepts.
* A **data model** connects various domain vocabularies to “connect the dots” with a specific purpose in mind.  Data models are specific to selected use cases or objectives.  A good data model leverages standard vocabularies often in the form of ontologies and defines and extends concepts and relationships only when necessary.<sup>2</sup>
* A **knowledge graph** is a data model populated with data.


[![Figure 1- DSPCore Data Model Overview Draft 1](https://github.com/DataBiosphere/terra-core-data-model/blob/master/documents/DSP%20Core%20Data%20Model%20Draft%201.jpg "Figure 1- DSPCore Data Model Overview Draft 1")](https://github.com/broadinstitute/dsp-data-models/blob/master/documents/DSP%20Core%20Data%20Model%20Draft%201.jpg "Figure 1- DSPCore Data Model Overview Draft 1")

### Status
DSPCore is currently under development and will be available in  RDF/XML and Turtle (.ttl) serializations.

### Versions
Stable Release Versions
Not yet available

### How did DSPCore Come About?

Since its founding, the Broad Institute has been involved in systematic efforts to create large datasets to serve as a foundation for biological and medical studies around the world.  These efforts require collecting data and their provenance, but also enabling researchers to find and reuse the data.  How do we do this as the volume, variety, and complexity of biomedical data increases?  At a minimum, we need to understand the data and how they are connected.  

Historically most biomedical data have been collected in silos as a side effect of source, project structure, research purpose, data type, funding, etc.  Through the Internet and cloud storage we increasingly have access to these massive datasets. 

The Broad Institute is committed to sharing data and knowledge. In defining data models, we aspire to the principles of the Data BioSphere<sup>3</sup> and the FAIR<sup>4</sup> guiding principles, notably:
* Open, community-driven, and standards-based data models
* Findable, accessible, interoperable, and reusable data

A number of national and international efforts have influenced our thinking in developing this data model.  To name only a few, we began by reviewing data models from Genomic Data Commons, Human Cell Atlas, NCBI Biosamples, and EMBL-EBI BioSamples.  (Please see Acknowledgements for a more complete list.)  When reviewing data models we found some focus on a particular subdomain, capturing more detail than we needed, while others are developed to address a different need.  We found that we were missing a cross-domain data model that could allow us to focus on our needs around search and finding data.  

We then formed a team of researchers within the Broad to ensure that the data model is consistent with the science.  If we follow the science, our data model will more accurately reflect the domain and enable researchers to find data using what are, for them, natural connections.  We recognize the need to create new relationships and add data points as time and science progress. 

Finally, we selected several datasets to test the model in our own pilot project.

### Using DSPCore
In addition to the formal specification in OWL (serialized in Turtle format), the Data Sciences Platform Team has defined a JSON representation of the Data Model that will be used internally at Broad Institute to pilot the data model.  This JSON representation is an example of how the data model can be used to design schemas for relational data.

### License
[BSD 3-Clause License](https://github.com/broadinstitute/dsp-data-models/blob/master/LICENSE)

### Contact
Please use this repository's [Issue Tracker](https://github.com/broadinstitute/dsp-data-models/issues "Issue Tracker") to share comments or concerns related to the data model.  DSPCore Data Model is not currently open to public contribution. DSPCore Data Model is currently wholly managed by Broad’s DSP Team.

### Acknowledgements
**Data Sciences Platform, Broad Institute**  
Dan Moran, Jeremy Hert, Ben Carlin, Raaid Arshad, Rori Cremer, Andrea Haessly, Jeff Korte, Emily Munro-Ludders, David Wine, Denis Loginov, and others.

**DSPCore Data Model Team**  
Larry Babb, Senior Principal Software Engineer  
Clare Bernard, PhD, Director of Product, Data Science Platform  
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



import random
import logging
from typing import Union

from sqlmodel import Session

from app import crud
from app.models.db import Item, ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_md5_string
from app.tests.utils.cath import random_cath_code
from app.models.db import DomainSummary
from app.models.chopping import ChoppingNumeric, SegmentNum

logger = logging.getLogger(__name__)

def create_random_uniprot_acc() -> str:
    return f"P{random.randint(0, 99999):05}"

def create_random_chopping_numeric(dom_id: str = None, is_multi: bool = None) -> ChoppingNumeric:
    if dom_id is None:
        dom_id = random_lower_string()

    if is_multi is None:
        is_multi = random.choice([True, False])

    if is_multi:
        num_segs = random.randint(2, 4)
        last_res_num = random.randint(1, 100)
        segs = []
        for _ in range(num_segs):
            start = random.randint(last_res_num, last_res_num+100)
            stop = random.randint(last_res_num+200, last_res_num+300)
            seg = SegmentNum(
                start=start,
                stop=stop,
            )
            last_res_num = stop
            segs.append(seg)
    else:
        segs = [SegmentNum(start=random.randint(100, 300), stop=random.randint(400, 600))]


    return ChoppingNumeric(
        domain_id=dom_id,
        segments=segs,
    )

def create_ted_id_string(uniprot_acc: str, domain_num: int) -> str:
    return f"AF-{uniprot_acc}-F1-model_v4_TED{domain_num:02}"


def create_random_domain_summary(uniprot_acc: str, 
                                 domain_num: int = 1, 
                                 ted_id: str = None,
                                 is_multi: bool = None, 
                                 cath_code: str = None, 
                                 plddt: float = None,
                                 chopping: Union[str|ChoppingNumeric] = None,
                                 md5=None) -> DomainSummary:

    if ted_id is None:
        ted_id=create_ted_id_string(uniprot_acc=uniprot_acc, domain_num=domain_num)

    if cath_code is None:
        cath_code = random_cath_code()
    if plddt is None:
        plddt = 50 + 50 * random.random()
    if md5 is None:
        md5 = random_md5_string()
    
    if chopping is None:
        chopping = create_random_chopping_numeric(is_multi=is_multi)
    elif isinstance(chopping, str):
        chopping = ChoppingNumeric.from_chopping_str(ted_id, chopping)
    elif not isinstance(chopping, ChoppingNumeric):
        raise ValueError(f"Invalid chopping: {chopping}")

    dom_summary = DomainSummary(
        ted_id=f"AF-{uniprot_acc}-F1-model_v4_TED{domain_num:02}",
        uniprot_acc=uniprot_acc,
        md5_domain=md5,
        consensus_level=random.choices(["high", "medium", "low"]),
        chopping=chopping.to_str(),
        nres_domain=chopping.count_residues(),
        num_segments=len(chopping.segments),
        plddt=plddt,
        num_helix_strand_turn=random.randint(0, 10),
        num_helix=random.randint(0, 10),
        num_strand=random.randint(0, 10),
        num_helix_strand=random.randint(0, 10),
        num_turn=random.randint(0, 10),
        proteome_id=random.randint(0, 70000),
        cath_label=cath_code,
        cath_assignment_level=random.choice(["H", "T", "A"]),
        cath_assignment_method=random.choice(["foldseek"]),
        packing_density=10 + random.random() * 20,
        norm_rg=random.random(),
        tax_common_name="-",
        tax_scientific_name=random.choice(["Streptomyces_viridosporus", "Streptomyces_griseus"]),
        tax_lineage="cellular_organisms,Bacteria,Terrabacteria_group,Actinomycetota,Actinomycetes,Kitasatosporales,Streptomycetaceae,Streptomyces",
    )
    return dom_summary

def create_random_domain_summary_entries(db: Session, uniprot_acc: str = None) -> Item:
    if uniprot_acc is None:
        uniprot_acc = "P12345"

    md5 = random_md5_string()

    dom_summary_entries = []
    for domain_num in range(2, 5):
        dom_summary = create_random_domain_summary(uniprot_acc, domain_num, md5=md5)
        db.add(dom_summary)
        dom_summary_entries.append(dom_summary)

    db.commit()
    return dom_summary_entries

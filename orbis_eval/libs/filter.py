def keep_entity(entity, annotations, gold_entities=None):
    if gold_entities is None:
        gold_entities = []
    if annotations:
        if _gold_contains_entity(entity, gold_entities, annotations):
            return True
        if _entity_contains_annotations(entity, annotations):
            return True
        return False
    return True


def _entity_contains_annotations(entity, annotations):
    for annotation in annotations:
        for annotation_filter in annotations[annotation]:
            if 'annotations' in entity:
                for annotation_entity in entity['annotations']:
                    if _contains_annotation(annotation_entity, annotation, annotation_filter):
                        return True
    return False


def _contains_annotation(annotation_entity, annotation, annotation_filter):
    return 'type' in annotation_entity and 'entity' in annotation_entity and \
           annotation_entity['type'] == annotation and \
           annotation_entity['entity'] == annotation_filter


def _gold_contains_entity(entity, gold_entities, annotations):
    if gold_entities:
        for gold_entity in gold_entities:
            if gold_entity['start'] == entity['document_start'] and gold_entity['end'] == entity['document_end'] and \
                    _entity_contains_annotations(gold_entity, annotations):
                return True
    return False

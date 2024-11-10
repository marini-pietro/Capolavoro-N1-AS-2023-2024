class CollisionManager:
    def __init__(self) -> None:
        ...
        
    def check_collision(self, entity_bound_box, block_bound_box) -> bool:
        """
        Check if the entity bounding box intersects with the block bounding box.

        Args:
            entity_bound_box (tuple[float]): The entity bounding box.
            block_bound_box (tuple[float]): The block bounding box.
        Returns:
            bool: True if the entity bounding box intersects with the block bounding box, False otherwise.
        """
        return self.bounding_boxes_intersect(entity_bound_box, block_bound_box)

    def bounding_boxes_intersect(self, bbox1, bbox2) -> bool:
        """
        Check if two bounding boxes intersect.
        
        Args:
            bbox1 (tuple[float]): The first bounding box.
            bbox2 (tuple[float]): The second bounding box.
        Returns:
            bool: True if the bounding boxes intersect, False otherwise.
        """

        min_x1, max_x1, min_y1, max_y1, min_z1, max_z1 = bbox1
        min_x2, max_x2, min_y2, max_y2, min_z2, max_z2 = bbox2

        return not (min_x1 <= max_x2 and max_x1 >= min_x2 and
                min_y1 <= max_y2 and max_y1 >= min_y2 and
                min_z1 <= max_z2 and max_z1 >= min_z2)
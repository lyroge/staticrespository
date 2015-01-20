UPDATE producttype p1 
        INNER JOIN producttype p2 
             ON p1.PARENTID = p2.ID
SET p1.ParentName = p2.NAME

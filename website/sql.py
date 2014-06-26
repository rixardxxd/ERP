__author__ = 'xxd'

class Sql:
    summary_sql = "select a.part_no,a.item_no,a.consignment as consignment, coalesce(b.sum,0) as usage_sum,coalesce(c.sum,0) as delivery_sum,coalesce(d.sum,0) as return_sum, NULLIF(a.sum,0) as total_sum from" \
     " (select website_otitem.part_no as part_no, website_otitem.item_no as item_no, website_otitem.consignment as consignment, SUM(amount) as sum from website_otitemdaily inner join website_otitem on website_otitemdaily.\"OTItem_id\" = website_otitem.id  "\
     " group by website_otitem.part_no,website_otitem.item_no, website_otitem.consignment) a " \
     " left join (select website_otitem.part_no as part_no, website_otitem.item_no as item_no, SUM(amount) as sum from website_otitemdaily inner join website_otitem on website_otitemdaily.\"OTItem_id\" = website_otitem.id " \
     " where website_otitemdaily.type = 'U' group by website_otitem.part_no,website_otitem.item_no) b on (a.part_no = b.part_no and a.item_no = b.item_no)" \
     " left join (select website_otitem.part_no as part_no, website_otitem.item_no as item_no, SUM(amount) as sum from website_otitemdaily inner join website_otitem on website_otitemdaily.\"OTItem_id\" = website_otitem.id" \
     " where website_otitemdaily.type = 'D' group by website_otitem.part_no,website_otitem.item_no) c on (a.part_no = c.part_no and a.item_no = c.item_no)" \
     " left join (select website_otitem.part_no as part_no, website_otitem.item_no as item_no, SUM(amount) as sum from website_otitemdaily inner join website_otitem on website_otitemdaily.\"OTItem_id\" = website_otitem.id" \
     " where website_otitemdaily.type = 'R' group by website_otitem.part_no,website_otitem.item_no) d on (a.part_no = d.part_no and a.item_no = d.item_no);"

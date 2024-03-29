__author__ = 'xxd'

class Sql:
    summary_sql = "select a.part_no as part_no, a.item_no as item_no, e.name as di_standard,a.size as size, a.consignment_amount as consignment_amount, coalesce(b.sum,0) as usage_sum,coalesce(c.sum,0) as delivery_sum,coalesce(d.sum,0) as return_sum from website_otitem a" \
            " left join (select website_otitemdaily.\"OTItem_id\", SUM(amount) as sum from website_otitemdaily where website_otitemdaily.type = 'U' group by website_otitemdaily.\"OTItem_id\") b on (a.id = b.\"OTItem_id\")" \
            " left join (select website_otitemdaily.\"OTItem_id\", SUM(amount) as sum from website_otitemdaily where website_otitemdaily.type = 'D' group by website_otitemdaily.\"OTItem_id\") c on (a.id = c.\"OTItem_id\")" \
            " left join (select website_otitemdaily.\"OTItem_id\", SUM(amount) as sum from website_otitemdaily where website_otitemdaily.type = 'R' group by website_otitemdaily.\"OTItem_id\") d on (a.id = d.\"OTItem_id\")" \
            " left join website_otdistandard e on (a.di_standard_id = e.id)" \
            " order by a.item_no;"
    monthly_usage_sql = "select a.part_no as part_no, a.item_no as item_no, f.name as di_standard,a.size as size, coalesce(b.sum,0) as history_sum, coalesce(c.sum,0) as current_month_sum,coalesce(d.sum,0) as second_month_sum,coalesce(e.sum,0) as third_month_sum from website_otitem a" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date < %s and type = 'U' group by \"OTItem_id\" ) b on (a.id = b.\"OTItem_id\")" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date = %s and type = 'U' group by \"OTItem_id\" ) c on (a.id = c.\"OTItem_id\")" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date = %s and type = 'U' group by \"OTItem_id\" ) d on (a.id = d.\"OTItem_id\")" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date = %s and type = 'U' group by \"OTItem_id\" ) e on (a.id = e.\"OTItem_id\")" \
                        " left join website_otdistandard f on (a.di_standard_id = f.id)" \
                        " order by a.item_no";
    monthly_return_sql = "select a.part_no as part_no, a.item_no as item_no, f.name as di_standard,a.size as size, coalesce(b.sum,0) as history_sum, coalesce(c.sum,0) as current_month_sum,coalesce(d.sum,0) as second_month_sum,coalesce(e.sum,0) as third_month_sum from website_otitem a" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date < %s and type = 'R' group by \"OTItem_id\" ) b on (a.id = b.\"OTItem_id\")" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date = %s and type = 'R' group by \"OTItem_id\" ) c on (a.id = c.\"OTItem_id\")" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date = %s and type = 'R' group by \"OTItem_id\" ) d on (a.id = d.\"OTItem_id\")" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date = %s and type = 'R' group by \"OTItem_id\" ) e on (a.id = e.\"OTItem_id\")" \
                        " left join website_otdistandard f on (a.di_standard_id = f.id)" \
                        " order by a.item_no";

    monthly_delivery_sql = "select a.part_no as part_no, a.item_no as item_no, f.name as di_standard,a.size as size, coalesce(b.sum,0) as history_sum, coalesce(c.sum,0) as current_month_sum,coalesce(d.sum,0) as second_month_sum,coalesce(e.sum,0) as third_month_sum from website_otitem a" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date < %s and type = 'D' group by \"OTItem_id\" ) b on (a.id = b.\"OTItem_id\")" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date = %s and type = 'D' group by \"OTItem_id\" ) c on (a.id = c.\"OTItem_id\")" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date = %s and type = 'D' group by \"OTItem_id\" ) d on (a.id = d.\"OTItem_id\")" \
                        " left join (select \"OTItem_id\",sum(amount) from website_otitemmonthly where date = %s and type = 'D' group by \"OTItem_id\" ) e on (a.id = e.\"OTItem_id\")" \
                        " left join website_otdistandard f on (a.di_standard_id = f.id)" \
                        " order by a.item_no";


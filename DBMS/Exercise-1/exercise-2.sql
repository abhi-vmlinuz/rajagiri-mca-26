drop table payment;
drop table sales;
drop table customer;
drop table purchase_item;
drop table purchase;
drop table product;
drop table category;
drop table supplier;
create table suppler (
	supplier_id varchar2(10) constraint sup_pk primary key,
	supplier_name varchar2(45) constraint sup_not_null not null,
	contact_person varchar2(20),
	mobile_no numeric,
	email_id varchar2(30) constraint sup_unique unique,
	address varchar2(60),
	city varhcar2(10)
);

create table category (
	category_id varchar2(10) constraint ctgry_pk primary key,
	category_name varchar2(30) constraint ctgry_not_null not null,
	constraint ctgry_unique unique(category_name),
	description varchar2(45)
);

create table product (
	product_id varchar2(10) constraint prdct_pk primary key,
	product_name varchar2(40) constraint prdct_nn not null,
	constraint prdct_frn_key foreign key (category_id) references category(category_id),
	constraint prdct_frn_key2 foreign key (supplier_id) references supplier(supplier_id),
	unit_price numeric(13,3) constraint prdct_check check ( unit_price > 0 ),
	reorder_level numeric constraint prdct_reorder_check check ( reorder_level > 0 ),
	quantity_available numeric constraint_prdct_quantity_check check ( quantity_available > 0 )
);

create table purchase (
	purchase_id varchar2(10) constraint prchse_pk primary key,
	constraint prchse_frn_key foreign key (supplier_id) references supplier(supplier_id),
	purchase_date date default current_date,
	total_amount numeric constraint prchse_check check (total_amount > 0 )
);

create table purchase_item (
	purchase_item_id varchar2(10) constraint prchse_item_pk primary key,
	constraint prchse_item_frn_key foreign key (purchase_id ) references purchase (purchase_id),
	constraint prchse_item_frn_key2 foreign key (product_id ) references product (product_id),
	quantity_purchased numeric constraint prchse_item_check check (quantity_purchased > 0 ),
	purchase_price numeric constraint prchse_price_check check (purchase_price > 0),
);

create table customer (
	customer_id varchar2(10) constraint cstmer_pk primary key,
	customer_name varchar2(45) constraint cstmer_nn not null,
	mobile_no numeric,
	email_id varchar2(40) constraint cstmer_uniq unique,
	address varchar2(50),
	city varchar(12)
);

create table sales (
		sales_id varchar2(10) constraint sales_pk primary key,
		constraint sales_frn_key foreign key (customer_id) references customer(customer_id),
		sales date default current_date,
		total_amount numeric constraint sales_check check (total_amount > 0),
		payment_status varchar2(10) constraint sales_check_2 check ( payment_status in ('PAID','UNPAID','PARTIAL'))
);

create table sales_item (
	sale_item_id varchar2(10) constraint sales_item_pk primary key,
	constraint sales_item_frn_key foreign key (sales_id) references sales(sales_id),
	constraint sales_item_frn_key2 foreign key (product_id) references product(product_id),
	quantity_sold numeric constraint sales_item_qty_check check (quantity_sold > 0),
	selling_price numeric constraint sales_item_selling_check check (selling_price > )
);

create table payment (
	payment_id numeric constraint payment_pk primary key,
	constraint payment_frn_key foreign key (sales_id) references sales(sales_id),
	payment_date date default current_date,
	amount_paid numeric constraint payment_check check (amount_paid > 0),
	payment_mode varchar2(10) constraint payment_mode check (payment_mode in ('CASH','CARD','UPI','BANK_TRANSFER'))
);

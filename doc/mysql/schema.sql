use thebest;

drop table if exists actions;
drop table if exists answers;
drop table if exists questions;
drop table if exists action_types;

create table if not exists questions
(
	id			char(40)	not null,
    question 	text 		not null,

    constraint pk_questions primary key (id),
    fulltext(question)

) engine=MyISAM;

create table if not exists answers
(
	question_id	char(40)	not null,
	id			char(40)	not null,
    answer 		text 		not null,

    constraint pk_answers primary key (question_id, id),
    constraint fk_answers__questions__question_id foreign key (question_id) references questions(id),
    fulltext(answer)

) engine=MyISAM;

create table if not exists action_types
(
    type		char(10)	not null,

    constraint pk_action_types primary key (type)
) engine=MyISAM;

insert into action_types values('VOTE');
insert into action_types values('SKIP');

create table if not exists actions
(
    id					int			not null auto_increment,
    
	question_id			char(40)	null,
    
	answer_question_id	char(40)	null,
	answer_id 			char(40)	null,

    type				char(10)	not null,
    ts 					timestamp 	default current_timestamp on update current_timestamp,

    constraint pk_actions primary key (id),
    constraint fk_actions__types__type foreign key (type) references action_types(type),
    constraint fk_actions__question__question_id foreign key (question_id) references questions(question_id),
    constraint fk_actions__answers__answer_id foreign key (answer_question_id, answer_id) references answers(question_id, id)
) engine=MyISAM;

create index idx_actions__question on actions(question_id);
create index idx_actions__answers on actions(question_id, answer_id);

/* initial data for testing */

insert into questions(id, question) values(sha1('auto para trabajar'), 'auto para trabajar');
insert into questions(id, question) values(sha1('restaurante para comer pastas'), 'restaurante para comer pastas');
insert into questions(id, question) values(sha1('lugar para comprar pastas'), 'lugar para comprar pastas');
insert into questions(id, question) values(sha1('restaurante chino'), 'restaurante chino');
insert into questions(id, question) values(sha1('auto para viajar'), 'auto para viajar');
insert into questions(id, question) values(sha1('carniceria carne cerdo'), 'carniceria carne cerdo');
insert into questions(id, question) values(sha1('carniceria'), 'carniceria');
insert into questions(id, question) values(sha1('panaderia'), 'panaderia');

insert into answers(question_id, id, answer) values(sha1('auto para trabajar'), sha1('volkswagen gol'), 'volkswagen gol');
insert into actions(answer_question_id, answer_id, type) values(sha1('auto para trabajar'), sha1('peugeot 206'), 'VOTE');
insert into actions(answer_question_id, answer_id, type) values(sha1('auto para trabajar'), sha1('peugeot 206'), 'VOTE');
insert into actions(answer_question_id, answer_id, type) values(sha1('auto para trabajar'), sha1('peugeot 206'), 'DISAGREE');
insert into actions(answer_question_id, answer_id, type) values(sha1('auto para trabajar'), sha1('peugeot 206'), 'DISAGREE');
insert into actions(answer_question_id, answer_id, type) values(sha1('auto para trabajar'), sha1('peugeot 206'), 'AGREE');

insert into answers(question_id, id, answer) values(sha1('auto para trabajar'), sha1('fiat uno'), 'fiat uno');
insert into actions(answer_question_id, answer_id, type) values(sha1('auto para trabajar'), sha1('fiat uno'), 'VOTE');

insert into answers(question_id, id, answer) values(sha1('auto para trabajar'), sha1('chevrolet corsa'), 'chevrolet corsa');
insert into actions(answer_question_id, answer_id, type) values(sha1('auto para trabajar'), sha1('chevrolet corsa'), 'VOTE');

insert into answers(question_id, id, answer) values(sha1('auto para trabajar'), sha1('ford k'), 'ford k');
insert into actions(answer_question_id, answer_id, type) values(sha1('auto para trabajar'), sha1('ford k'), 'VOTE');

insert into answers(question_id, id, answer) values(sha1('auto para trabajar'), sha1('peugeot 206'), 'peugeot 206');
insert into actions(answer_question_id, answer_id, type) values(sha1('auto para trabajar'), sha1('peugeot 206'), 'VOTE');

insert into answers(question_id, id, answer) values(sha1('restaurante para comer pastas'), sha1('la pirola'), 'la pirola');
insert into actions(answer_question_id, answer_id, type) values(sha1('restaurante para comer pastas'), sha1('la pirola'), 'VOTE');
insert into answers(question_id, id, answer) values(sha1('restaurante para comer pastas'), sha1('Mamma Mía'), 'Mamma Mía');
insert into actions(answer_question_id, answer_id, type) values(sha1('restaurante para comer pastas'), sha1('Mamma Mía'), 'VOTE');

insert into answers(question_id, id, answer) values(sha1('lugar para comprar pastas'), sha1('polidori'), 'polidori');
insert into actions(answer_question_id, answer_id, type) values(sha1('lugar para comprar pastas'), sha1('polidori'), 'VOTE');
insert into answers(question_id, id, answer) values(sha1('lugar para comprar pastas'), sha1('san cayetano'), 'san cayetano');
insert into actions(answer_question_id, answer_id, type) values(sha1('lugar para comprar pastas'), sha1('san cayetano'), 'VOTE');

/* Some queries */

/* To search a question*/

select *
  from questions
 where MATCH(question) AGAINST('+pan*' IN BOOLEAN MODE);

select *
  from questions
 where MATCH(question) AGAINST('+pasta*' IN BOOLEAN MODE);

select *
  from questions
 where MATCH(question) AGAINST('+tr*' IN BOOLEAN MODE);

select *
  from questions
 where MATCH(question) AGAINST('+au*' IN BOOLEAN MODE);


/* To search a answer*/

select *
  from answers
 where question_id = 1
   and MATCH(answer) AGAINST('+vol*' IN BOOLEAN MODE);

select *
  from answers
 where question_id = 1
   and MATCH(answer) AGAINST('+gol*' IN BOOLEAN MODE);


/* To get the question whitout responses*/

select q.id, q.question, count(*), max(a.ts)
  from questions q
	left join answers a
		on q.id = a.question_id
group by q.id, q.question


select q.id as question_id,
	   a.id as answer_id,
	   a.answer,
	   (select count(*)
		  from actions ac
		 where ac.answer_question_id = q.id) as votes
 from questions q 
	join answers a
      on a.question_id = q.id
order by votes desc



select sha1(question), question
  from questions

select * from actions;

select id,
	   question,
	   (select count(*)
		  from actions a
		 where a.answer_question_id = q.id) as votes,
	   (select max(ts)
		  from actions a
		 where a.answer_question_id = q.id) as last_vote
 from questions q
order by votes, last_vote

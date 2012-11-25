package org.python.util;

import net.sf.jsqlparser.*;
import net.sf.jsqlparser.expression.*;
import net.sf.jsqlparser.expression.operators.arithmetic.*;
import net.sf.jsqlparser.expression.operators.conditional.*;
import net.sf.jsqlparser.expression.operators.relational.*;
import net.sf.jsqlparser.parser.*;
import java.io.StringReader; //hopefully this works
import net.sf.jsqlparser.schema.*;
import net.sf.jsqlparser.statement.*;
import net.sf.jsqlparser.statement.create.table.*;
import net.sf.jsqlparser.statement.delete.*;
import net.sf.jsqlparser.statement.drop.*;
import net.sf.jsqlparser.statement.insert.*;
import net.sf.jsqlparser.statement.replace.*;
import net.sf.jsqlparser.statement.select.*;
import net.sf.jsqlparser.statement.truncate.*;
import net.sf.jsqlparser.statement.update.*;
import net.sf.jsqlparser.util.deparser.*;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.DatabaseMetaData;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import oracle.jdbc.OracleConnection;
import oracle.jdbc.OracleResultSet;
import oracle.jdbc.pool.OracleDataSource;

import org.python.core.SPARQLDoer;
import org.python.util.SQLValidator; // added

import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.lang.String;
import java.lang.Character;
import java.text.DecimalFormatSymbols;
import java.util.Arrays;

public class SQLVisitor implements SelectVisitor, FromItemVisitor, ExpressionVisitor, ItemsListVisitor, SelectItemVisitor, OrderByVisitor {
	private List<String> filters;
	private List<String> tables;
	private List<String> columns;
	private List<String> columnsNoDot;
	private List<String> matches;
	private List<String> orderby;
	private List<String> subselects;
	private HashMap<String, String> tablesAliases;
	private LinkedHashMap<String, String> columnsAs;
	private List<String> internalColumns;
	private String temp;
	private String ownException;
	private Boolean wasEquals;
	private Boolean subselect;
	
	private static int joinInc = 1; // for each join this will be incremented and used in a variable name.
	public String site;
	
	private static String tablenameFrom = "";
	public static String url = "";
	public static String uname = "";
	public static String pword = "";
	public static OracleDataSource ods;
	public static OracleConnection connection;
	public static Statement stmt;
	public static SPARQLDoer sd;
	public static SQLValidator validator; // added to vlidate sql
	public String saveName = "";
	

	CCJSqlParserManager parserManager = new CCJSqlParserManager();

	public SQLVisitor(OracleConnection conn, String url, String uname, String pword) {
		this.url = url;
		this.uname = uname.toUpperCase();
		this.pword = pword; 
		this.connection = conn;
		this.sd = new SPARQLDoer(conn, uname);
	}

	public void doDrop(Drop stmt, OracleConnection conn) {
		String tableToDrop = stmt.getName();
		String website = "www.example.org/";
		String command = "";

		if ( tableToDrop.equals("RDF_DATA") ) {
			System.out.println("Dropping the RDF model and everything associated with it: " + tableToDrop);
			//Do the RDF data drop of models and everything else
			try {
                        	conn.createStatement().executeQuery("DROP SEQUENCE RDF_DATA_TABLE_SQNC");
			} catch (SQLException e) {
				System.out.println("Failed to drop RDF data table sequence\n" + e);
			}
                        try {
				conn.createStatement().executeQuery("DROP SEQUENCE RDF_GUID_SQNC");       
			} catch (SQLException e) {
				System.out.println("Failed to drop RDF GUID sequence\n" + e);
			}
			try {
                        	conn.createStatement().executeQuery("BEGIN\nSEM_APIS.DROP_RDF_MODEL('RDF_MODEL_" + uname.toUpperCase() + "');\nEND;");
			} catch (SQLException e) {
				System.out.println("Failed to drop RDF model: RDF_MODEL_" +uname.toUpperCase() + "\n" + e);
			}
			try {
                        	conn.createStatement().executeQuery("DROP TABLE RDF_DATA_TABLE");
			} catch (SQLException e) {
				System.out.println("Failed to drop RDF data table\n" + e);
			}

		} else {

			System.out.println("Dropping just one named graph from the RDF data: " + tableToDrop);
			command = "DELETE from RDF_DATA_TABLE a where a.triple.GET_MODEL() = 'RDF_MODEL_" + uname.toUpperCase()  + ":<" + website + tableToDrop + ">'";
			try {
				conn.createStatement().executeQuery(command);
				System.out.println("|" + command + "|");
			} catch (SQLException e) {
				System.out.println("Failed to drop RDF named graph: " + tableToDrop);
				System.out.println(e);
			}
		}

	}

    public void getInsert(Insert stmt, OracleConnection conn) throws SQLException {
        String individual = "";
        String dataType = "";
        String tmpString = "";
        String namedGraph = "RDF_MODEL_" + uname + ":<" + stmt.getTable() + ">";

        if (stmt.getColumns() != null) {

            individual = sd.getNextAnonNodeForInd();
            sd.insertDVAMetaData(uname, namedGraph, individual, stmt.getTable().toString());

            Iterator valsIt = ((ExpressionList)stmt.getItemsList()).getExpressions().iterator();
            for (Iterator colsIt = stmt.getColumns().iterator(); colsIt.hasNext(); ) {
                Column col = (Column)colsIt.next();

                dataType = sd.getType(col.getColumnName());
                tmpString = valsIt.next().toString();

                // this if statement removes the leading and trailing single quotes from strings and dates
                if (dataType.endsWith("string")) {
                    tmpString = tmpString.substring(1, tmpString.length() - 1);
                    dataType = "\"" + tmpString + "\"" + dataType;
                } else if (dataType.endsWith("date")) {
                    if (tmpString.toUpperCase().equals("NULL") || tmpString.equals("''")) {
                        dataType = "NULL" + dataType;
                    } else {
                        tmpString = tmpString.substring(1, tmpString.length() - 1);
                        dataType = "\"" + tmpString + "\"" + dataType;
                    }
                } else if (dataType.endsWith("unknown")) {
                    dataType = tmpString.replaceAll("'", "");
                } else {
                    dataType = "\"" + tmpString + "\"" + dataType;
                }
                
                sd.insertDataPropQuadSQL(individual,col.getColumnName(), dataType);
            }
        }
    }

    public void getCreateTable(CreateTable stmt, OracleConnection conn) throws SQLException {
        String modelName = "RDF_MODEL_" + uname;
        String tableName = stmt.getTable().getName();
        //String namedGraph = "<www.example.org/" + tableName + ">";
        String namedGraph = tableName;
        String attribute;
        String type;
        String xsdType;

        sd.createQuadStore(modelName);
        sd.insertObjectPropQuad(namedGraph, "rdf:type", "rdfs:Class");

        if (stmt.getColumnDefinitions() != null) {
            for (Iterator colsIt = stmt.getColumnDefinitions().iterator(); colsIt.hasNext(); ) {
                ColumnDefinition col = (ColumnDefinition)colsIt.next();
                attribute = col.getColumnName();
                type = col.getColDataType().getDataType();

                if (type.toLowerCase().equals("numeric") || type.toLowerCase().equals("decimal") ||
                    type.toLowerCase().equals("real")) {
                    xsdType = "xsd:decimal"; // was decimal
                } else if (type.toLowerCase().equals("varchar") || type.toLowerCase().equals("varchar2")) {
                    xsdType = "xsd:string"; // was string
                } else if (type.toLowerCase().equals("bit") || type.toLowerCase().equals("tinyint") ||
                           type.toLowerCase().equals("bigint")) {
                    xsdType = "xsd:integer"; // was integer
                } else if (type.toLowerCase().equals("date")) {
                    xsdType = "xsd:date"; // was integer
                } else {
                    xsdType = "xsd:decimal"; // was decimal
                }

                sd.insertObjectPropQuad(attribute, "rdf:type", "owl:DatatypeProperty");
                sd.insertObjectPropQuad(attribute, "rdfs:domain", namedGraph);
                sd.insertObjectPropQuad(attribute, "rdf:range", "rdfs:" + xsdType);
            }
        }
    }

	public String getSelect(Select select) throws SQLException, JSQLParserException, ownIllegalSQLException{
		//System.out.println("SQLVisitor:206 - inside getSelect(Select select).");		
		
		validator = new SQLValidator(); // added
		
		boolean debugging = true;
		String s = "SELECT ";
		
		site = "www.example.org/"; 

		filters = new ArrayList<String>();
		tables = new ArrayList<String>();
		matches = new ArrayList<String>();
		orderby = new ArrayList<String>();
		subselects = new ArrayList<String>();

		select.getSelectBody().accept(this);
		
		//System.out.println(select.getWithItemsList());
		//for(Iterator i=select.getWithItemsList().iterator(); i.hasNext();) {
			//WithItem withItem = (WithItem)i.next();	//columns.add(withItem.getName());
		//}
		if(debugging){
			printList("Filters:", filters, false);
			printList("Tables:", tables, false);
			printList("Columns:", null, true);
			printList("Internal Columns:", internalColumns, false);
			printList("Matches (or Joins?):", matches, false);
			printList("Order By:", orderby, false);
			printList("Subselects:", subselects, false);
		}
		System.out.println("\n\n");
		
		try{
			if(!ownException.equals("")){
				throw new ownIllegalSQLException(ownException);
			}
		} catch (ownIllegalSQLException e){
			System.out.println(e);
			return e.toString();
		}
		
		//System.out.println(Arrays.toString(columnsAs.entrySet().toArray()));
		
		//creating columns for ORACLE SQL from regular SQL statement,
		//current part to create, e.g. SELECT E.A AS CS345, G.B CS370 FROM D AS E, F AS G ...
		//will result in SELECT A_D CS345, B_F CS370 FROM TABLE( SEM_MATCH('SELECT * WHERE {
		//note aliases mapping for table names where done while "visiting"
		for (String entry : columnsAs.keySet()) {
			s += colname(entry) + "_" + tablename(entry) + " " +colname(columnsAs.get(entry)) + ", ";
		}
		
		s = s.substring(0,s.length()-2);
		s += " from table(\n\tSEM_MATCH('SELECT * WHERE {\n\t";
		
		//Following example from above SPARQL query will looks like:
		//	?thisD rdf:type :D .
		//	?thisD :A ?A_D .
		//	?thisF rdf:type :F .
		//	?thisF :B :B_F
		String currTable = "";
		for (String item : columnsAs.keySet()) {
			String tableName = tablename(item);
			String colName = colname(item);
			String tempTableName = tableName;
			if(!tempTableName.equals(currTable)){
				s += "?this" + tempTableName + " rdf:type :" + tableName + " . \n\t";
				currTable = tempTableName;
			}
			s += "?this" + tempTableName + " :" + colName + " ?" + colName + "_" + tempTableName + " . \n\t";	//}
		}
		
		//Adding JOINS, e.g.FROM D AS E JOIN F AS G ON E.STUDENID = G.STUDENTID
		//will result in:	?thisD :STUDENTID ?j1 . ?thisF :STUDENTID ?j1 .
		for(Iterator fI=matches.iterator(); fI.hasNext();) {
			String item = (String)fI.next();
			s += item + "\n\t";
		}
		
		// Adding the filters to SEM_MATCH, e.g WHERE D.GRADES > 80
		//results in: FILTER( GRADES_D > 80)
		if ( !filters.isEmpty() ) {
			for(Iterator fI=filters.iterator(); fI.hasNext();) {
				String item = (((String)fI.next()).trim()).split("\\s+")[0];
    			int lio_ = item.lastIndexOf("_");
    			String col = item.substring(0, lio_).replace("?", "");
    			String tName = item.substring(lio_ + 1);
				if(!columnsAs.containsKey(tName + "." + col)){
    				s += "?this" + tName + " :" + col + " " + item + " .\n\t";
				}
			}
			
			//for(int i = 0; i < filters.size();i++)
				//System.out.println("Filter " + i + " " + filters.get(i));
			
			// want to print out Filters in RDF ONLY if we are at the bottom of a subselect, OR
			// if there are two filters and one is  not a subselect, then print just that one.	
			
			if (subselects.isEmpty() || filters.size() > 1) {
							
				//if filter list has multiple items and there are subselects, only print the filters that don't contian " ".			
				if(filters.size() > 1 && !subselects.isEmpty()) { // added
				s += "FILTER ( ";
					/*for(Iterator fI=filters.iterator(); fI.hasNext();) {
						
						String item = (String)fI.next();
						if(!item.contains("\"")); {
							s += item + " ";
							if (fI.hasNext()) {
								s += " && ";
							}
						}
					} */
					String item = (String)filters.get(0);
					s += item + " ";
					s += " ) ";
				}				
				else {				
					s += "FILTER ( ";
					for(Iterator fI=filters.iterator(); fI.hasNext();) {
						String item = (String)fI.next();
						s += item + " ";
						if (fI.hasNext()) {
							s += " && ";
						}
					}
					s += " ) ";
				}
			}
		}
		
		
		//INTERNAL COLUMNS
		for (String item : internalColumns) {
			String tableName = tablename(item);
			String colName = colname(item);
			s += "?this" + tableName + " :" + colName + " ?" + colName + "_" + tableName + " . \n\t";
		}
		
		//working on progress...
		s += "}";
		// Adding order by to SEM_MATCH
		if(orderby.size()>0) {
			s += "\n\t ORDER BY ";
			for(Iterator fI=orderby.iterator(); fI.hasNext();) {
				String item = (String)fI.next();
				s += item + " ";
			}
		}
		//Adding model and alias to ORACLE SQL statement
		s += "',\n\t SEM_MODELS('RDF_MODEL_" + uname + "'), ";
		s += "null,\n\t SEM_ALIASES( SEM_ALIAS('', 'http://www.example.org/people.owl#')), null) )";
		
		//int i = 0;
		//for(String subSel: subselects) {
			//System.out.println("subselect element " + i +" is " + subSel);
		//}
		
		if(!subselects.isEmpty()) {		
			
			for(Iterator fI=subselects.iterator(); fI.hasNext();) {
						
				// if we are in a subselect, doesn't the first and only other filter in the filter
				// list have to be the original where? 	
				
							
				String firstFilter = filters.get(filters.size() - 1);    /*String firstFilter = filters.get(0); original*/				
                int equalSign = firstFilter.indexOf('='); // get index of = sign to know where to stop
				int questionMark = firstFilter.indexOf('?');  // get index of ? in case it's not the first character in filter
				firstFilter = firstFilter.substring(questionMark + 1, equalSign - 1);
				String newS = "\n\twhere " + firstFilter + "  in ("; 
				net.sf.jsqlparser.statement.select.Select caststmt = null;
				
				try {	
				   //System.out.println(" In try block of subselect 356.");			
					net.sf.jsqlparser.statement.Statement statement = null;
					statement = (net.sf.jsqlparser.statement.Statement)parserManager.parse(new StringReader((String)fI.next()));		
					caststmt = (net.sf.jsqlparser.statement.select.Select)statement;
				} catch (Exception e) {
					System.out.println("SQLVisitor. 330. Exception: " + e.toString());
				}
				
				newS += getSelect(caststmt);
								
				//String item = (String)fI.next();
				s += newS + " ";
				if (fI.hasNext()) {
					s += "\n";
				}
			}
			s+= ")";

		}
		//System.out.println("RDF conversion of select:\n |" + s + "|");		
		//printList("field", filters, false);
		return s;
	}
	public void printList(String field, List<String> list, boolean isHashMap){ 
		System.out.println(field);
		if(isHashMap)
			for (String entry : columnsAs.keySet()) {
				System.out.println("\t"+entry);
			}
		else	
			for(Iterator fI=list.iterator(); fI.hasNext();) {
				System.out.println("\t"+fI.next());
			}
	}
	
	
	static public String tablename(String item) {
		if(item.indexOf('.')>0)
			return item.substring(0,item.indexOf('.'));
		return "tbl";
	}
	
	// ?BIRTH_YEAR_PETS = PETS.BIRTH_YEAR
	static public String getFilterTableName(String str) {
		String newString = str.substring(0, str.indexOf(" "));
		return newString.substring(newString.lastIndexOf("_") + 1);
        // return (str.substring(0, str.indexOf(" "))).substring(str.lastIndexOf("_") + 1);
    }
	static public String colname(String item) {
		if(item.indexOf('.')>0)
			return item.substring(item.indexOf('.')+1);
		return item;
	}
	
	static public String filter(String item, String comparison, String value) {
		String tempTableName = tablename(item);
		return "?" + colname(item) + "_" + tempTableName + " " + comparison + " "  + value;
	}
	
	static public String match(String item, String value, boolean isValue) {
		String joinString = "";
		String tablename = tablename(item);
		if(isValue) {
			// this is the case of columName = someValue
			return " ?" + colname(item) + "_" + tablename + " = " + value;
		} else {
			// this is the case of joining two tables
			// first half of join 
			joinString += "?this" + tablename + " :" + colname(item) + " ?j" + joinInc + " . ";
			// second half of join
			tablename = tablename(value);
			joinString += "?this" + tablename + " :" + colname(value) + " ?j" + joinInc + " . ";
			joinInc++;

			return joinString;
		}
	/*	if(isValue)
			return "?"+tablename(item)+" "+tablename(item)+":"+colname(item)+" "+tablename(item)+":"+value;
		return "?"+tablename(item)+" "+tablename(item)+":"+colname(item)+" ?"+tablename(value)+colname(value);
	*/
	}
	static public List<String> getAllColsFromTbl(String tableName) throws SQLException, JSQLParserException{
		List<String> tCols = new ArrayList<String>();
		List<String> temp = sd.getAllColumns(uname,tableName);
		for(Iterator fI=temp.iterator(); fI.hasNext();) {
			
			String c = (String)fI.next();
			if(!c.equals("type"))
				tCols.add(c);
		}
		//System.out.println(Arrays.toString(tCols.toArray()));
		return tCols;
	}
	public void visit(PlainSelect plainSelect) { 
		//System.out.println("SQLVisitor:384 - inside visit(PlainSelect plainSelect).");	
	
		ownException = "";
		//will contain <nameOfTable, columnsOfTable>
		HashMap<String, List<String>> tablesColumns = new HashMap<String, List<String>>();
		
		//FROM thisTable AS a will be store as <a, thisTable>
		tablesAliases = new HashMap<String,String>();
		
		//SELECT thisColumn AS col will be store as <thisColumn, col>
		columnsAs = new LinkedHashMap<String,String>();
		
		internalColumns = new ArrayList<String>();
		
		//Adding table from FROM clause
		FromItem t = plainSelect.getFromItem(); //Accepting the visitor
		t.accept(this);
		String alias = t.getAlias();
		tables.add(temp);
		
		if(alias == null) 
			tablesAliases.put(temp,temp);  
		else 
			tablesAliases.put(alias,temp);
			
		//Get column names from current added table, will help on mapping aliases
		try{	
			tablesColumns.put(temp, getAllColsFromTbl(temp));	
		} catch (JSQLParserException e) {	
			System.err.println("Caught JSQLParserException: " + e.getMessage());	
		} catch (SQLException e) {	
			System.err.println("Caught SQLException: " + e.getMessage());	
		}
		
		//plainSelect is the whole statement
		if (plainSelect.getJoins() != null) {
			for (Iterator joinsIt = plainSelect.getJoins().iterator(); joinsIt.hasNext();) {
				Join join = (Join) joinsIt.next();
				t = join.getRightItem();
				t.accept(this);
				
				//right side of JOIN needs to be stored as a table, proceed as previously 
				alias = t.getAlias();
				tables.add(temp);
				try{	
					tablesColumns.put(temp, getAllColsFromTbl(temp));	
				} catch (JSQLParserException e) {	
					System.err.println("Caught JSQLParserException: " + e.getMessage());	
				} catch (SQLException e) {	
					System.err.println("Caught SQLException: " + e.getMessage());	
				}
				if(alias == null) 
					tablesAliases.put(temp,temp); 
				else 
					tablesAliases.put(alias,temp);
				
				//joins...
				if(join.getOnExpression() != null) {
					join.getOnExpression().accept(this);
					//at this point, the temp just gets converted to the rhs side of the ON expression
					//LEFT SIDE OF JOIN
					String tableName = temp.substring(5, temp.indexOf(" :"));
					
					/*String key = tableName;
					
					if(!tablesAliases.containsKey(key))					
						key = (String)getKeyByValue(tablesAliases,tableName);
					if(key == null || !key.equals(tableName)){
						ownException = "ORA-00904: \""+tableName+"\": invalid identifier";
						return;
					}*/
					
					if(!(ownException = validator.validateTable(tablesAliases, tableName, "")).isEmpty()){
						return;
					}
					
					
					temp = temp.replace(tableName, tablesAliases.get(tableName));
					//RIGHT SIDE OF JOIN
					tableName = temp.substring(temp.lastIndexOf("?this") + 5, temp.lastIndexOf(" :"));
					/*
					key = tableName;
					if(!tablesAliases.containsKey(key))
						key = (String)getKeyByValue(tablesAliases,tableName);
					if(key == null || !key.equals(tableName)){
						ownException = "ORA-00904: \""+tableName+"\": invalid identifier";
						return;
					}*/
					
					if(!(ownException = validator.validateTable(tablesAliases, tableName, "")).isEmpty()){
						return;
					}
					
					temp = temp.replace(tableName, tablesAliases.get(tableName));
					matches.add(temp);
					
				}
			}
		}
		
		if(plainSelect.getSelectItems() != null) {
			//gets the columns that are asked of
			for(Iterator i=plainSelect.getSelectItems().iterator(); i.hasNext();) {
				SelectItem item = (SelectItem)i.next();
				item.accept(this);
				// if selecting everything
				if(temp.equals("*")){
					for(Iterator fI=tables.iterator(); fI.hasNext();) {
						String tbl = (String)fI.next();
						//Get all columns from requested table
						for(Iterator fII=tablesColumns.get(tbl).iterator(); fII.hasNext();){
							String c = (String)fII.next();
							columnsAs.put(tbl + "." + c,tbl + "." + c);
						}
					}
				}
				else{
					String tempColumnAs = "";
					Boolean columnAs = false;
					
					if(item.toString().contains(" AS ")){
						String[] split = (item.toString()).split(" AS ");
						tempColumnAs = split[1];
						columnAs = true;
					}
					
					String tableName = tablename(temp);
					String colName = "";
					
					if(tableName.equals("tbl")){
						//validate column
						colName = validator.validateColumn(tablesColumns, colname(temp));
						if(!validator.isValidColumn()){
							ownException = colName;
							return;
						}
					}
					else{
						//Validate column
						if(!(ownException = validator.validateTable(tablesAliases, tableName, colname(temp))).isEmpty()){
							return;
						}
						
				 		//put the column in proper format
						if(tablesAliases.containsKey(tableName))
							colName = temp.replace(tableName, tablesAliases.get(tableName));
						else{
							colName = temp;
						}
					}
					if(columnAs)
						columnsAs.put(colName,tempColumnAs);
					else
						columnsAs.put(colName,colName);
				}
			}
					
		}
		
		if (plainSelect.getWhere() != null) {                                //ie, there's a where clause
			wasEquals = false;
			
			// if whereclause is a select, don't visit yet
			//System.out.println("Printing out plainSelect.getWhere():  " + plainSelect.getWhere().toString());
			plainSelect.getWhere().accept(this);
			//System.out.println("Returned from subdselect?");
			
			//System.out.println("temp= " + temp);
			String tableName = getFilterTableName(temp.trim());
			//System.out.println("Built tableName");
			String key = tableName;
			//String[] whereStrings = plainSelect.getWhere().toString().split(" ");
			//System.out.println("about to build saveName");
			//for(int i = 0; i < whereStrings.length; i++)
				//if(whereStrings[i].toUpperCase().equals("(SELECT"))
					//saveName = whereStrings[0] + "_";
			//System.out.println("saveName: " + saveName);
					//System.out.println("Made it : 605");
			String dataValue = temp.substring(temp.lastIndexOf(" ") + 1);
					//System.out.println("Made it :607");
			if(!isNumeric(dataValue))
				temp =temp.substring(0, temp.lastIndexOf(" ") + 1) + "\"" + temp.substring(temp.lastIndexOf(" ") + 1) + "\"";
			//System.out.println("Made it : 610");
			if(!key.equals("tbl")){
				//validate table name
				if(!(ownException = validator.validateTable(tablesAliases, tableName, temp.substring(temp.indexOf("?")+1,temp.lastIndexOf("_")))).isEmpty()){
					return;
				}
						//System.out.println("Made it : 618");
				if(tablesAliases.containsKey(tableName)){
					filters.add(temp.replace(tableName, tablesAliases.get(tableName)));
				/*	if (saveName != null) {
						saveName = saveName + "" + tableName;
						System.out.println("\n\n\nSAVENAME == " + saveName + "\n\n");
					}
				*/}
			}
			else{
				String ct = temp.trim().split("\\s+")[0];
				String col = ct.substring(1, ct.lastIndexOf("_"));
				
				//validate column
				String colName = validator.validateColumn(tablesColumns, col);
				if(!validator.isValidColumn()){
					ownException = colName;
					return;
				}
				tableName = tablename(colName);
				filters.add(temp.replace("_tbl","_" + tableName));
			}
		}
			/*
			if(wasEquals) { //OK EQUAL STATEMENTS ARE NOT MATCHES, BUT FILTERS?
				matches.add(temp);
				filters.add(temp);
			}
			*/
	
		
		
		if(plainSelect.getOrderByElements() != null) {
			for(Iterator i=plainSelect.getOrderByElements().iterator(); i.hasNext();) {
				OrderByElement item = (OrderByElement)i.next();
				item.accept(this);
				if(!(temp.contains("DESC") || temp.contains("ASC"))){
					//System.out.println("HERE 658");
					String tableName = tablename(temp);
					String key = tableName; 
					if(!(ownException = validator.validateTable(tablesAliases, tableName, colname(temp))).isEmpty()){
						return;
					}
					if(tablesAliases.containsKey(tableName))
						orderby.add(temp.replace(tableName, tablesAliases.get(tableName)));
					else
						orderby.add(temp);
				}
				else{
					temp = temp.trim();
					String colName = temp.substring(temp.indexOf(" ?") + 2, temp.lastIndexOf("_"));
					String tName = temp.substring(temp.lastIndexOf("_") + 1, temp.lastIndexOf(" )"));
					if(tName.equals("tbl")){
						//Validate column
						colName = validator.validateColumn(tablesColumns, colName);
						if(!validator.isValidColumn()){
							ownException = colName;
							return;
						}
						temp = temp.replace("tbl", tablename(colName));
					}
					if(!columnsAs.containsKey(tName+ "." + colName)){
						internalColumns.add(tName+ "." + colName);
					}
					
					orderby.add(temp);
				}
			}
		}
	}
	
	
	static public boolean isNumeric(String str){
		DecimalFormatSymbols currentLocaleSymbols = DecimalFormatSymbols.getInstance();
		char minusSign = currentLocaleSymbols.getMinusSign();

		if (!Character.isDigit(str.charAt(0)) && str.charAt(0) != minusSign) 
			return false;

		boolean isDecimal = false;
		char decimalSeparator = currentLocaleSymbols.getDecimalSeparator();

		for (char chr : str.substring(1).toCharArray()){
			if(!Character.isDigit(chr)){
				if(chr == decimalSeparator && !isDecimal){
					isDecimal = true;
					continue;
				}
				return false;
			}
		}
		return true;
	}
	static public String getKeyByValue(HashMap<String, String> map, String value) {
		for (String entry : map.keySet()) {
			if (map.get(entry).equals(value)) {
				return entry;
			}
		}
		return null;
	}
	public void testMethod(String sub) {
		try {
			PlainSelect plainSelect2 = (PlainSelect) ((Select) parserManager.parse(new StringReader(sub))).getSelectBody();        	
			//System.out.println("Plainselect2 : " + plainSelect2);
			visit(plainSelect2);
			}
		catch (JSQLParserException e) {
			System.out.println("Null");
			//return null;
		}

	}

	public void visit(Union union) {
		for (Iterator iter = union.getPlainSelects().iterator(); iter.hasNext();) {
			PlainSelect plainSelect = (PlainSelect) iter.next();
			visit(plainSelect);
		}
	}

	public void visit(Table tableName) {
		temp = tableName.getWholeTableName();
	}
	
	// Added
	public void visit(SubSelect subSelect) {
		
	try {		
		CCJSqlParserManager pm = new CCJSqlParserManager();
		net.sf.jsqlparser.statement.Statement statement = null;
		       
		// turn temp subselect into a normal sqlstmt (remove parens)
		//String sqlstmt2 = "SELECT VISITS.VETID FROM VISITS WHERE VISITS.VETID = 4001";
		int i = 0;
		String subSelString = subSelect.toString();
		int frontParen = subSelString.indexOf('(');
		int backParen = subSelString.lastIndexOf(')');
		subSelString = subSelString.substring((frontParen+1), backParen);
		
		
		
		statement = (net.sf.jsqlparser.statement.Statement)pm.parse(new StringReader(subSelString));
		
		net.sf.jsqlparser.statement.select.Select caststmt = (net.sf.jsqlparser.statement.select.Select)statement;
		
		subselects.add(caststmt.toString());
	
		} catch (Exception e) {
		System.out.println("sqlvisitor:740:In catch block of of subselcet...");
	    }
	}

	public void visit(Addition addition) {
		addition.getLeftExpression().accept(this);
		String t = "(" + temp;
		t += addition.getStringExpression();
		addition.getRightExpression().accept(this);
		t += temp + ") ";
		temp = t;
	}

	public void visit(AndExpression andExpression) {
		wasEquals = false;
		andExpression.getLeftExpression().accept(this);
		if(wasEquals) {
			matches.add(temp);
		} else {
			String tableName = getFilterTableName(temp);
			String key = tableName;
			if(!key.equals("tbl")){
				if(!(ownException = validator.validateTable(tablesAliases, tableName, temp.substring(temp.indexOf("?")+1,temp.lastIndexOf("_")))).isEmpty()){
					return;
				}
				if(tablesAliases.containsKey(tableName))
					filters.add(temp.replace(tableName, tablesAliases.get(tableName)));
			}
			else{
				tableName = validator.validateColumnAs(columnsAs, temp);
				if(!validator.isValidColumn()){
					ownException = tableName;
					return;
				}
				filters.add(temp.replace("_tbl","_" + tableName));
			}
		}
		wasEquals = false;
		andExpression.getRightExpression().accept(this);
	}

	public void visit(Between between) {
		between.getLeftExpression().accept(this);
		between.getBetweenExpressionStart().accept(this);
		between.getBetweenExpressionEnd().accept(this);
	}

	public void visit(Column tableColumn) {
		temp = tableColumn.getWholeColumnName();
	}

	public void visit(Division division) {
		division.getLeftExpression().accept(this);
		String t = "(" + temp;
		t += division.getStringExpression();
		division.getRightExpression().accept(this);
		t += temp + ") ";
		temp = t;
	}

	public void visit(DoubleValue doubleValue) {
		temp = Double.toString(doubleValue.getValue());
	}
	public void visit(EqualsTo equalsTo) {
		equalsTo.getLeftExpression().accept(this);
		String item = temp;
		String comparison = "";
		equalsTo.getRightExpression().accept(this);
		if(equalsTo.getRightExpression() instanceof Column) {
			 temp = match(item, temp, false);
		} else {
			temp = match(item, temp, true);
		}
		wasEquals = true;
	}

	public void visit(Function function) {
	}

	
	public void visit(GreaterThan greaterThan) {
		greaterThan.getLeftExpression().accept(this);
		String item = temp;
		String comparison = "";
		if(greaterThan.isNot()) {
			comparison = "<=";
		} else {
			comparison = ">";
		}
		greaterThan.getRightExpression().accept(this);
		String value = temp;
		temp = filter(item, comparison, value);
	}

	public void visit(GreaterThanEquals greaterThanEquals) {
		greaterThanEquals.getLeftExpression().accept(this);
		String item = temp;
		String comparison = "";
		if(greaterThanEquals.isNot()) {
			comparison = "<";
		} else {
			comparison = ">=";
		}
		greaterThanEquals.getRightExpression().accept(this);
		String value = temp;
		temp = filter(item, comparison, value);
	}

	public void visit(InExpression inExpression) {
		inExpression.getLeftExpression().accept(this);
		String t = temp + " IN ";
		inExpression.getItemsList().accept(this);
		t += temp;
		temp = t;
	}

	public void visit(InverseExpression inverseExpression) {
		inverseExpression.getExpression().accept(this);
	}

	public void visit(IsNullExpression isNullExpression) {
	}

	public void visit(JdbcParameter jdbcParameter) {
	}

	public void visit(LikeExpression likeExpression) {
		visitBinaryExpression(likeExpression);
	}

	public void visit(ExistsExpression existsExpression) {
		existsExpression.getRightExpression().accept(this);
	}

	public void visit(LongValue longValue) {
		temp = longValue.getStringValue();
	}

	public void visit(MinorThan minorThan) {
		minorThan.getLeftExpression().accept(this);
		String item = temp;
		String comparison = "";
		if(minorThan.isNot()) {
			comparison = ">=";
		} else {
			comparison = "<";
		}
		minorThan.getRightExpression().accept(this);
		String value = temp;
		temp = filter(item,comparison, value);
	}

	public void visit(MinorThanEquals minorThanEquals) {
		minorThanEquals.getLeftExpression().accept(this);
		String item = temp;
		String comparison = "";
		if(minorThanEquals.isNot()) {
			comparison = ">";
		} else {
			comparison = "<=";
		}
		minorThanEquals.getRightExpression().accept(this);
		String value = temp;
		temp = filter(item, comparison, value);
	}

	public void visit(Multiplication multiplication) {
		multiplication.getLeftExpression().accept(this);
		String t = "(" + temp;
		t += multiplication.getStringExpression();
		multiplication.getRightExpression().accept(this);
		t += temp + ") ";
		temp = t;
	}

	public void visit(NotEqualsTo notEqualsTo) {
		notEqualsTo.getLeftExpression().accept(this);
		String item = temp;
		String comparison = "!=";
		notEqualsTo.getRightExpression().accept(this);
		String value = temp;
		/*
		if(notEqualsTo.getRightExpression() instanceof Column)
			value += "?"+tablename(temp)+colname(temp);
		else
			value += temp;
		*/
		temp = filter(item, comparison, value);
	}

	public void visit(NullValue nullValue) {
		temp = nullValue.toString();
	}

	public void visit(OrExpression orExpression) {
		orExpression.getLeftExpression().accept(this);
		String left = temp;
		orExpression.getRightExpression().accept(this);
		temp = "FILTER( "+left+" || "+temp+" )";
		wasEquals = false;
	}

	public void visit(Parenthesis parenthesis) {
		String t = "";
		if(parenthesis.isNot())
			t += "!";
		parenthesis.getExpression().accept(this);
		t += "("+temp+")";
		temp = t;
	}

	public void visit(StringValue stringValue) {
		temp = stringValue.getValue();
	}

	public void visit(Subtraction subtraction) {
		subtraction.getLeftExpression().accept(this);
		String t = "(" + temp;
		t += subtraction.getStringExpression();
		subtraction.getRightExpression().accept(this);
		t += temp + ") ";
		temp = t;
	}

	public void visitBinaryExpression(BinaryExpression binaryExpression) {
		binaryExpression.getLeftExpression().accept(this);
		binaryExpression.getRightExpression().accept(this);
	}

	public void visit(ExpressionList expressionList) {
		String t = "(";
		for (Iterator iter = expressionList.getExpressions().iterator(); iter.hasNext();) {
			Expression expression = (Expression) iter.next();
			expression.accept(this);
			t += temp + ", ";
		}
		t = t.substring(0, t.length()-2) + ")";
		temp = t;

	}

	public void visit(DateValue dateValue) {
		temp = dateValue.getValue().toString();
	}
	
	public void visit(TimestampValue timestampValue) {
		temp = timestampValue.getValue().toString();
	}
	
	public void visit(TimeValue timeValue) {
		temp = timeValue.getValue().toString();
	}

	public void visit(CaseExpression caseExpression) {
	}

	public void visit(WhenClause whenClause) {
	}
	
	public void visit(BitwiseXor bitwiseXor) {
	}
	
	public void visit(BitwiseOr bitwiseOr) {
	}
	
	public void visit(BitwiseAnd bitwiseAnd) {
	}
	
	public void visit(Matches matches) {
	}
	
	public void visit(Concat concat) {
	}

	public void visit(AllComparisonExpression allComparisonExpression) {
		allComparisonExpression.GetSubSelect().getSelectBody().accept(this);
	}

	public void visit(AnyComparisonExpression anyComparisonExpression) {
		anyComparisonExpression.GetSubSelect().getSelectBody().accept(this);
	}

	public void visit(SubJoin subjoin) {
		subjoin.getLeft().accept(this);
		subjoin.getJoin().getRightItem().accept(this);
	}
	
	//SELECT ItemS
	public void visit(AllColumns columns) {
		temp = "*";
	}
	
	public void visit(AllTableColumns columns) {
		temp = "*";
	}
	
	public void visit(SelectExpressionItem item) {
		item.getExpression().accept(this);
	}
	
	//Order by visitor
	public void visit(OrderByElement order) {
		order.getExpression().accept(this);
		if(order.isAsc()) {
			temp = " ASC( ?" + colname(temp) + "_" + tablename(temp) + " )";
		} else {
			temp = " DESC( ?" + colname(temp) + "_" + tablename(temp) + " )";
		}
		/*
		if(!order.isAsc()) {
			temp = "DESC(?"+tablename(temp)+colname(temp)+")";
		} else {
			temp = "ASC(?"+tablename(temp)+colname(temp)+")";
		}
		*/
	}
	private class ownIllegalSQLException extends IllegalArgumentException
	{
	public ownIllegalSQLException( String message )
	{
	  super( message );
	}
	}

}

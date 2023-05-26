<?php

include( "../../localconfig.php" );
include( "includes/fusioncharts.php" );

  //Finding Active Taps
  $participantId = $_POST["participantId"];
  $startDate = $_POST["startDate"];
  $endDate = $_POST["endDate"];
  $arrayResults;
  $map;

  function findActiveTaps($interactions, $entryArray, $eventArray){

    /*
    Add new to-do list item: Count number of “create” entries in Events table
    Edit preexisting to-do list item: Count number of “edit” entries in Events table
    Add new journal entry: Count number of “create” entries with entryType=”journal” in Entries table
    Edit preexisting journal entry: Count number of “edit” entries with entryType=”journal” in Entries table
    Add new notes entry: Count number of “create” entries with entryType=”note” in Entries table
    Edit preexisting notes entry: Count number of “edit” entries with entryType=”note” in Entries table
    View calendar tab: Count number of “present” entries with elementId=4 in interactions table
    Use Help button: Count number of “tap” entries with elementId=12 or 42 in interactions table
    View, add, and/or edit Profile page:
      Count number of “present” entries with elementId=5 in interactions table, plus
      Count number of “tap” entries with elementId=22 in interactions table
    */
    $numActiveTaps = 0;
    $newToDo = 0;
    $editToDo = 0;
    $addJournal = 0;
    $editJournal = 0;
    $addNote = 0;
    $editNote = 0;
    $viewCal = 0;
    $useHelp = 0;
    $profile = 0;

    foreach($interactions as $interactionEntry){

      $interactionType = $interactionEntry['interaction'];
      $id = $interactionEntry['elementId'];

      if($interactionType == "present"){
        if($id == 4){
          $viewCal++; //View Calendar Tab: if "present" and elementId == 4
        }
        if($id == 5){
          $profile++; //View/Add and/or edit profile page: if "present" and elementId == 5
        }
      }else{
        if($id == 12 || $id == 14){
          $useHelp++; //Use help button: if "tap" and elementId == 12, 14
        }
        if($id == 22){
          $profile++; //View/Add and/or edit profile page: if "tap" and elementId == 22
        }
      }

    }

    foreach($entryArray as $entry){
      $type = $entry['entryType'];
      $action = $entry['action'];

      if($type == "note"){
        if($action == "create"){
          $addNote++;
        }else{
          $editNote++;
        }
      }else{
        if($action == "create"){
          $addJournal++;
        }else{
          $editJournal++;
        }
      }

    }

    foreach($eventArray as $events){
      $action = $events['action'];
      //"todo" or "scheduled"
      if($action == "create"){
        $newToDo++;
      }else{
        $editToDo++;
      }

    }

    $numActiveTaps = $newToDo + $editToDo + $addJournal + $editJournal + $addNote + $editNote + $viewCal + $useHelp + $profile;

    $arrayResults = array(
                      "newToDo" => "$newToDo",
                      "editToDo" => "$editToDo",
                      "addJournal" => "$addJournal",
                      "editJournal" => "$editJournal",
                      "addNote" => "$addNote",
                      "editNote" => "$editNote",
                      "viewCalender" => "$viewCal",
                      "useHelp" => "$useHelp",
                      "profile" => "$profile"

                    );
      // echo("From function: " . $numActiveTaps . "\n");

      return $arrayResults;
  }

  function getTotalActiveTaps($array){
    $total = 0;
    foreach($array as $key => $value){
      $total += $value;
    }

    $arrayResults = array("Total Active Taps " => "$total");
    return $arrayResults;

  }

  ////// Function for Graphing Part //////
  function MapAssocArray ($array) {
      // Converts data returned from SQL query to a form acceptable to FusionCharts
      $result = array();
      foreach($array as $key => $value){
        //print $key . ": " . $value . "</br>";

        $temp = array();
        $temp["label"] = $key;
        $temp["value"] = $value;
        array_push($result, $temp);

      }
      return $result;
  }
  //////////////////////////////////////

  function findDistinctUses($interactions) {
      $total = 0;
      $perDay = 0;
      $prev = null;

      //For graph
     $prevDate = NULL;
     $totalPerDay = 0;
     $i = 0;
     $arrayResults = array();
     $array = array();
      foreach ($interactions as $interaction) {
        $timestamp_local = $interaction['timestamp_local'];
        $i++;

        $diff = abs(strtotime($timestamp_local) - strtotime($prev));
        $diffMin = ($diff / 60); //difference in minutes
        //print "</br> " . $diffMin;

        if($diffMin > 5.0){
          //if inactivity is greater than 5 min == new use
          // print "Greater than 5min";
          $interactionId = $interaction['interactionId'];
          $total++;

          //For Line Graph
          $dateFormatted = date("M/d", strtotime($timestamp_local));

            if($prevDate == $dateFormatted || $prevDate == NULL){
              $totalPerDay++;
            }else{
              // $totalPerDay++;
              $temp = array();
              $temp["label"] = $prevDate;
              $temp["value"] = $totalPerDay;
              array_push($arrayResults, $temp);
              $totalPerDay = 1;
            }
        }else{
          //recheck
          if($prevDate != $dateFormatted && $prevDate != NULL){
            $temp = array();
            // $dateChart = array("label" => "$prevDate", "value" => "$totalPerDay");
            // print $dateChart["label"] . ": " . $dateChart["value"];
            $temp["label"] = $prevDate;
            $temp["value"] = $totalPerDay;
            array_push($arrayResults, $temp);
          }
        }

        if($i == count($interactions) - 1){
          $dateFormatted = date("M/d", strtotime($timestamp_local));

          $temp = array();
          $temp["label"] = $dateFormatted;
          $temp["value"] = $totalPerDay;
          array_push($arrayResults, $temp);
          // $totalPerDay = 1;
        }

        $prev = $timestamp_local;
        $prevDate = date("M/d", strtotime($timestamp_local));
      }

      $array = array("Distinct Uses" => $totalPerDay);
      return $array;
  }


  // function MapAssocMilestone ($array) {
  //                // Converts data returned from SQL query to a form acceptable to FusionCharts
  //                // $result = array();
  //                //
  //                // foreach($array as $key => $value){
  //                //   $result()
  //                // }
  //                // echo(var_dump($array["context2"]));
  //                // $label = $array["context2"];
  //                // $value
  //                // $result["label"] = $array["context2"];
  //                // $result["value"] = $array["COUNT(*)"];
  //                // $result($array["context2"] => $array["COUNT(*)"]);
  //                // return $result;
  // }

  function eventTimes($events){
    $numEvents = count($events);
    $prospective = 0;
    $retrospective = 0;
    $todoCurrent= 0;
    $scheduledCurrent = 0;
    $completed = 0;

    $recurring = 0;
    $reminderPrior = 0;
    $reminderAtEvent = 0;

    foreach($events as $event){
      $timestamp = $event["timestamp_local"];
      $typeEvent = $event["eventType"];
      $sTime = $event["startTime"];
      $eTime = $event["endTime"];
      $participant = $event["participantId"];
      $eDate = $event["eventDate"];
      $id = $event["eventId"];
      $t = $event["eventToken"];
      $act = $event ["action"];
      $comp = $event["completed"];

      $recurring += $event["recurring"];
      $reminderPrior += $event["reminderPrior"];
      $reminderAtEvent += $event["reminderAtEvent"];

      $cdt = strtotime($timestamp);
      $sdt = strtotime($eDate);
      $startTm = strtotime($sTime);
      $endTm = strtotime($eTime);
      $cdate = date('m/d/Y', $cdt);
      $sdate = date('m/d/Y', $sdt);
      $stm = date('H:i:s', $startTm);
      $etm = date('H:i:s', $endTm);
      $ctm = date('H:i:s', $cdt);

      if($comp == 1){
       $completed = $completed+1;
      }

      if ($typeEvent == 'scheduled' && $act != 'delete'){
        if ($cdate < $sdate){
          $prospective = $prospective +1;
        }
        if ($cdate > $sdate){
         $retrospective = $retrospective +1;

        }
        if($cdate == $sdate){
           if($ctm > $etm){
             $retrospective = $retrospective +1;
          }
           if($ctm < $stm){
            $prospective = $prospective +1;
          }
          if ($ctm <= $etm && $ctm >= $stm){
            $scheduledCurrent = $scheduledCurrent +1;
          }
        }
      } elseif ($typeEvent == 'todo' && $act != 'delete'){
        if ($cdate < $sdate){
          $prospective++;
        }
        if ($cdate > $sdate){
         $retrospective++;
        }
        if($cdate == $sdate){
          $todoCurrent = $todoCurrent +1;
        }
      }
    }

  // print "<h1>retrospective($retrospective)</h1>";
  // print "<h1>prospective($prospective)</h1>";
  // print "<h1>current($todoCurrent)</h1>";
  // print "<h1> scheduledCurrent($scheduledCurrent)";
  // print "<h1> completedEvents ($completed)";
  $arrayResults = array(
                   "Total Events" => "$numEvents",
                   "Retrospective" => "$retrospective",
                   "Prospective" => "$prospective",
                   "CurrentTodo" => "$todoCurrent",
                   "CurrentSchedule" => "$scheduledCurrent",
                   "Completed Events" => "$completed",
                   "Recurring Events" => "$recurring",
                   "Reminder(s) Set Before Event" => "$reminderPrior",
                   "Reminder(s) Set On Event" => "$reminderAtEvent"
                 );
   return $arrayResults;
  }

  function noteEntries($entries, $interactions) {
    $createdNotes = 0 ;
    $createdJournals = 0;
    $edittedJournals = 0;
    $edittedNotes = 0;
    $deletedNotes = 0;
    $deletedJournal = 0;
    $deletedTodo = 0;
    $totalCharNotes = 0;
    $totalWordsNotes = 0;
    $totalCharJournal = 0;
    $totalWordsJournal = 0;
    $titleWords = 0;
    $entryWords= 0;
    $textLength = 0;
    $titleLength = 0;

    // print count($interactions) . "</br>";
    foreach($interactions as $interaction){
      // print $interaction['entryId'] . " )  " . $interaction['entryToken'] . ", " . $interaction['timestamp_local'] ."</br>";
      $texLength = strlen($interaction['content']);
      $tLength = strlen($interaction['title']);
      $eWords = str_word_count($interaction['content']);
      $tWords = str_word_count($interaction['title']);

      if($interaction['entryType'] == "note"){
        $titleWords = $titleWords + $tWords;
        $titleLength = $titleLength +$tLength;
        $noteentryWords = $entryWords + $eWords;
        $notetextLength = $textLength +$texLength;
      }else{
        $journalentryWords = $entryWords + $eWords;
        $journaltextLength = $textLength +$texLength;
      }
    }

    foreach ($entries as $entry) {
      $entryId= $entry['entryType'];
      $entryParticipant = $entry['participantId'];
      $entryText= $entry['content'];
      $entryAction= $entry['action'];
      $entryTitle = $entry['title'];

      switch ($entryId){
        case "journal":
          if($entryAction =='create'){
            $createdJournals = $createdJournals +1;

          }
          if($entryAction =='edit'){
            $edittedJournals = $edittedJournals +1;
          }
          if($entryAction == 'delete'){
            $deletedJournal = $deletedJournal +1;
          }
          break;
        case "note":
          if($entryAction =='create'){
            $createdNotes = $createdNotes +1;
          }
          if($entryAction =='edit'){
            $edittedNotes = $edittedNotes +1;
          }
          if($entryAction == 'delete'){
            $deletedNotes = $deletedNotes +1;
          }
          break;
      }
    }

    $mixedtotalWord = $noteentryWords + $journalentryWords + $titleWords;
    $mixedtotalChar = $notetextLength + $journaltextLength + $titleLength;

    // print "<h2>Number of Created Notes = $createdNotes</h2>";
    // print "<h2> Number of Created Journals = $createdJournals</h2>";
    // print "<h2>Number of editted Notes = $edittedNotes</h2>";
    // print "<h2> Number of editted Journals = $edittedJournals</h2>";
    // print "<h2> Deleted Journals($deletedJournal)</h2>";
    // print "<h2> Deleted Notes($deletedNotes)</h2>";
    // print "Total Word Count (Journal & Note & Title): " . $mixedtotalWord . "</br>";
    // print "Total Character Count (Journal & Note & Title): " . $mixedtotalChar . "</br>";
    // print "Total Character Count (Notes): " . $notetextLength . "</br>";
    // print "Total Character Count (Journal): " . $journaltextLength . "</br>";
    // print "Total Word Count (Notes): " . $noteentryWords . "</br>";
    // print "Total Word Count (Journal): " . $journalentryWords . "</br>";
    // print "Total Title Word Count (Note): " . $titleWords . "</br>";
    // print "Total Title Character Count (Journal): " . $titleLength . "</br>";

    $arrayResults = array(
                     "Num Created Notes" => "$createdNotes",
                     "Num Created Journals" => "$createdJournals",
                     "Num Edited Notes" => "$edittedNotes",
                     "Num Edited Journals" => "$edittedJournals",
                     "Num Deleted Notes" => "$deletedNotes",
                     "Num Deleted Journals" => "$deletedJournal",
                     "Total Word Count" => "$mixedtotalWord",
                     "Total Character Count" => "$mixedtotalChar",
                     "Total Character Count (Notes)" => "$notetextLength",
                     "Total Character Count (Journals)" => "$journaltextLength",
                     "Total Word Count (Notes)" => "$noteentryWords",
                     "Total Word Count (Journals)" => "$journalentryWords",
                     "Total Title Word Count" => "$titleWords",
                     "Total Title Character Count" => "$titleLength",
                   );

    return $arrayResults;
  }

  function dataArray($interactions){
    $numbermilestones = 0;
    $dismissedMile = 0;
    $milestoneAccomp = 0;
    $trainingAlarm = 0;

    foreach($interactions as $interaction){
      $elementType = $interaction["elementType"];
      $action = $interaction["context3"];
      $from = $interaction["context2"];
      $typeAlert = $interaction["context1"];
      $participant = $interaction["participantId"];

      switch ($typeAlert){
        case "milestoneAlert":
          if ($from == 'dismiss'){
            $dismissedMile = $dismissedMile + 1;
          }
          if ($from == 'recordAccomplishment'){
            $milestoneAccomp = $milestoneAccomp +1;
          }
          $numbermilestones = $numbermilestones +1;
          break;
        case 'trainingAlert':
          $trainingAlarm = $trainingAlarm +1;
          break;
      }
    }

  // print ("<h2> milestoneAlerts($numbermilestones)</h2>");
  // print ("<h3> recordedMilestoneAccomplishments($milestoneAccomp)</h3>");
  // print ("<h3> dismissedMilestoneAccomplishments($dismissedMile)</h3>");
  // print ("<h2> trainingAlarm($trainingAlarm)</h2>");

  $arrayResults = array(
                   "Total Milestone Alerts" => "$numbermilestones",
                   "Num Recorded Milestone Accomplishments" => "$milestoneAccomp",
                   "Num Dismissed Milestone Accomplishments" => "$dismissedMile",
                   "Total Training Alarms" => "$trainingAlarm",

                 );

  return $arrayResults;

  }

  function getArray1($dbh, $participantId, $startDate, $endDatePlus){
    // echo($startDate);


      //Getting active taps
      $elementId = $dbh->prepare ("SELECT elementId, interaction FROM interactions WHERE participantId = ? AND timestamp_local >= '$startDate' AND timestamp_local <= '$endDatePlus'");
      $elementId->execute([$participantId]);
      $interactions = $elementId->fetchAll(PDO::FETCH_ASSOC);

      // echo("sizeof interactions" . sizeof($interactions));
      //Getting entries
      $entries = $dbh->prepare ("SELECT entryType, action FROM entries WHERE participantId = ? AND (action = 'create' OR action = 'edit') AND timestamp_local >= '$startDate' AND timestamp_local <= '$endDatePlus' ");
      $entries->execute([$participantId]);
      $entryArray = $entries->fetchAll(PDO::FETCH_ASSOC); //array of entries

      //Getting events
      $events = $dbh->prepare ("SELECT action FROM events WHERE participantId = ? AND (action = 'create' OR action = 'edit') AND timestamp_local >= '$startDate' AND timestamp_local <= '$endDatePlus'");
      $events->execute([$participantId]);
      $eventArray = $events->fetchAll(PDO::FETCH_ASSOC); //array of events

      $arrayResults = findActiveTaps($interactions, $entryArray, $eventArray); //returns array for graph
      // $dataArray = MapAssocArray($arrayResults);
      return $arrayResults;

  }

  function getArray2($dbh, $participantId, $startDate, $endDatePlus){

    // Getting total number of taps and calculating number of distinct taps
            $statement = $dbh->prepare ("SELECT interactionId, timestamp_local, interaction FROM interactions WHERE participantId = ? AND (interaction = 'tapped' OR interaction = 'tap') AND timestamp_local >= '$startDate' AND timestamp_local <= '$endDatePlus'");
            $statement->execute([$participantId]);
            $interactions = $statement->fetchAll(PDO::FETCH_ASSOC); // associative array (dictionary)
    // print $participantId . ", " . $type . ", " . $startDate . ", " . $endDatePlus;
            $arrayResults = findDistinctUses($interactions);
            // $dataArray = $arrayResults;
            // print count($arrayResults);
      return $arrayResults;

  }

  function getArray3($dbh, $participantId, $startDate, $endDatePlus){
    $statement = $dbh->prepare ("SELECT elements.context2, elements.context1,  COUNT(*) FROM interactions
                                                       INNER JOIN elements ON elements.elementId = interactions.elementId WHERE participantId = ? AND timestamp_local >= '$startDate' AND timestamp_local <= '$endDatePlus' AND context1 =
                                                       'milestoneAlert' GROUP BY interactions.elementId ");
    $statement->execute([$participantId]);
    $results = $statement->fetchAll(PDO::FETCH_ASSOC);
    // echo(sizeof($results) . "<br>");

    $arrayResults = array();
    $arrayResults2 = array();
    $flag = true;
    // echo($results[0]["context2"]);
    foreach($results[0] as $key => $value){
      // echo($key . "</br>" . $results["context2"]);
      if($results[0]["context2"] == "dismiss"){
        $arrayResults = array("Dismiss" => $value);
      }else{
        $flag = false;
        $arrayResults = array("Dismiss" => 0);
        $arrayResults2 = array("Record Accomplishments" => $value);
      }
    }

    if(sizeof($results) == 2){
      foreach($results[1] as $key => $value){
        $arrayResults2 = array("Record Accomplishments" => $value);
      }
    }else{
      if($flag == true){
        $arrayResults2 = array("Record Accomplishments" => 0);
      }
    }

    return $arrayResults + $arrayResults2;

  }

  function getArray4($dbh, $participantId, $startDate, $endDatePlus){
    $eventArray = $dbh->prepare ("SELECT * FROM events WHERE participantId = ? AND timestamp_local >= '$startDate' AND timestamp_local <= '$endDatePlus' AND timestamp_local in (Select max(timestamp_local) FROM events group by eventToken)");
            $eventArray->execute([$participantId]);
            $eventArray2 = $eventArray->fetchAll(PDO::FETCH_ASSOC); //array of events
            $arrayResults = eventTimes($eventArray2); //returns array for graph
            // $dataArray = MapAssocArray($arrayResults);
    return $arrayResults;

  }

  function getArray5($dbh, $participantId, $startDate, $endDatePlus){
    $arrayResults = getOverall(); //returns array for graph
    // $dataArray = MapAssocArray($arrayResults);
    return $arrayResults;

  }

  function getArray6($dbh, $participantId, $startDate, $endDatePlus){
    $statement = $dbh->prepare ("SELECT interactionId, timestamp_local, interaction FROM interactions WHERE participantId = ? AND (interaction = 'tapped' OR interaction = 'tap') AND timestamp_local >= '$startDate' AND timestamp_local <= '$endDatePlus'");
    $statement->execute([$participantId]);
    $interactions = $statement->fetchAll(PDO::FETCH_ASSOC); // associative array (dictionary)
    // print " <h2> Total Number of Taps: " . count($interactions) . " </h2>";

    $arrayResults = array("Total Taps" => count($interactions));

    return $arrayResults;

  }

  //entries
  function getArray7($dbh, $participantId, $startDate, $endDatePlus){
    $statement = $dbh->prepare ("SELECT * FROM entries  WHERE participantId = ? AND timestamp_local >= '$startDate' AND timestamp_local <= '$endDatePlus' "); //Gets all entries within date range
    $statement->execute([$participantId]);
    $interactions = $statement->fetchAll(PDO::FETCH_ASSOC); // associative array

    //Gets all unique entries within date range
    $wordc = $dbh->prepare ("SELECT * from entries where participantId = ? AND timestamp_local in (Select max(timestamp_local) FROM entries WHERE timestamp_local >= '$startDate' AND timestamp_local <= '$endDatePlus' AND (action = 'create' OR action = 'edit') group by entryToken)  ");

    $wordc->execute([$participantId]);
    $wordInter = $wordc->fetchAll(PDO::FETCH_ASSOC); // associative array
    $arrayResults = noteEntries($interactions, $wordInter);

    $totalEntries = array("Total Entries" => count($wordInter)); // !!THIS NUM IS WRONG, CHECK AGAIN
    return $arrayResults; // +$totalEntries
  }

  function getArray8($dbh, $participantId, $startDate, $endDatePlus){
    $statement = $dbh->prepare("SELECT elements.context1, elements.context2 FROM interactions
                                INNER JOIN elements ON elements.elementId = interactions.elementId WHERE interactions.participantId = ? AND interactions.timestamp_local >= '$startDate' AND interactions.timestamp_local <= '$endDatePlus'");
    $statement->execute([$participantId]);
    $interactions = $statement->fetchAll(PDO::FETCH_ASSOC); // associative array
    $arrayResults = dataArray($interactions);

    return $arrayResults; // +$totalEntries
  }

  try {


    //Getting Summary Data into one associative array
      // PDO (PHP Data Object), connects to the database
      $dbh = getDatabaseHandle($dbhost, $dbname, $dbuser, $dbpass);

      $start = date('Y-m-d', strtotime("$startDate"));

      $endDatePlus = date('Y-m-d', strtotime("+1 day", strtotime("$startDate"))); //Needs to be the day after to include data during the lastest date
      $endDatePlus2 = date('Y-m-d', strtotime("+1 day", strtotime("$endDate")));

      $diff = abs(strtotime($endDatePlus2) - strtotime($start));
      $diffDays = (int) floor(($diff/60)/1440);

      $result = array();
      $startDateTemp = $startDate;

      for($i = 0; $i < $diffDays; $i++){
        $idArray = array("Participant ID" => $participantId);
        $dateArray = array("Date" => $startDateTemp);

        $startDatePlus = date('Y-m-d', strtotime("+1 day", strtotime("$startDateTemp")));

        $totalTaps = array();
        $totalTaps = getArray6($dbh, $participantId, $startDateTemp, $startDatePlus); //total taps
        $map = array();
        $map = getArray1($dbh, $participantId, $startDateTemp, $startDatePlus); //active taps detail
        $map2 = array();
        $map2 = getArray2($dbh, $participantId, $startDateTemp, $startDatePlus);
        $map3 = array();
        $map3 = getArray3($dbh, $participantId, $startDateTemp, $startDatePlus);
        $map4 = array();
        $map4 = getArray4($dbh, $participantId, $startDateTemp, $startDatePlus);
        $map7 = array();
        $map7 = getArray7($dbh, $participantId, $startDateTemp, $startDatePlus);
        $map8 = array();
        $map8 = getArray8($dbh, $participantId, $startDateTemp, $startDatePlus);
        // $map5 = array();
        // $map5 = getArray5($dbh, $participantId, $startDate, $endDatePlus);
        // // echo("Size of Map: " . sizeof($map) . "<br>");
        // // array_merge($result, $map);

        $numActiveTapsArray = getTotalActiveTaps($map);

        $result2 = $idArray + $dateArray + $totalTaps + $numActiveTapsArray + $map + $map2 + $map3 + $map4+ $map7 + $map8; // + $map3 + $map4 + $map5
        // // $result3 = $dateArray + $map;
        array_push($result, $result2);
        // echo("Size of Result: " . sizeof($result) . " <br>");
        // echo("Result: " . $result2["Date"] . "<br>");
        // echo($result["newToDo"]);
        $startDateTemp = date('Y-m-d', strtotime("+1 day", strtotime("$startDateTemp")));

      }

//Converting to CSV
      $fileName =  "Summary_Data_" . $participantId;

      if ($result) {
          // Export CSV file
          $fileName .= ".csv";
          header("Content-Type: text/csv; charset=utf-8");
          header("Content-Disposition: attachment; filename=\"$fileName\"");
          $output = fopen("php://output", "w");
          // Get headers
          $headers = array();
          foreach ($result[0] as $key => $value) {
              // echo $key;
              array_push($headers,$key);
          }
          fputcsv($output, $headers);
          foreach ($result as $row) {
              $rowData = array();
              foreach ($headers as $key) { // Make sure we get the values in the same order as headers
                  array_push($rowData,$row[$key]);
              }
              fputcsv($output, $rowData);
          }
          fclose($output);
      } else {
          throw new Exception("No data exists for these parameters.", 400);
      }


  } catch ( Exception $e ) {
      print($e->getMessage());
  }


  ?>

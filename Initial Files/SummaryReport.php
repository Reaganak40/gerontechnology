<?php

namespace App\Entity;

class SummaryReport
{
    private $scheduledEvents;
    private $nonScheduledEvents;
    private $highPriorityEvents;
    private $repeatedEvents;
    private $phyExEvents;
    private $mentExEvents;
    private $wbExEvents;
    private $completedScheduledEvents;
    private $completedNonScheduledEvents;
    private $completedHighPriorityEvents;
    private $completedRepeatEvents;
    private $completedPhyExEvents;
    private $completedMentExEvents;
    private $completedWbExEvents;
    private $numTotalFolders;
    private $numTotalNotes;
    private $numItemsInCalendar;
    private $hiddenEventsCount;
    private $amountPhyEx;
    private $amountMentEx;
    private $amountWbEx;
    private $scheduledEventsWordCount;
    private $nonScheduledEventsWordCount;
    private $scheduledEventsCharacterCount;
    private $nonScheduledEventsCharacterCount;
    private $functZonesWordCount;
    private $ltGoalsWordCount;
    private $userNotesWordCount;
    private $functZonesCharacterCount;
    private $ltGoalsCharacterCount;
    private $userNotesCharacterCount;
    private $wbJournalWordCount;
    private $wbJournalCharacterCount;

    public function __construct()
    {
        $this->scheduledEvents = 0;
        $this->nonScheduledEvents = 0;
        $this->highPriorityEvents = 0;
        $this->repeatedEvents = 0;
        $this->phyExEvents = 0;
        $this->mentExEvents = 0;
        $this->wbExEvents = 0;
        $this->completedScheduledEvents = 0;
        $this->completedNonScheduledEvents = 0;
        $this->completedHighPriorityEvents = 0;
        $this->completedRepeatEvents = 0;
        $this->completedPhyExEvents = 0;
        $this->completedMentExEvents = 0;
        $this->completedWbExEvents = 0;
        $this->numTotalFolders = 0;
        $this->numTotalNotes = 0;
        $this->numItemsInCalendar = 0;
        $this->hiddenEventsCount = 0;
        $this->amountPhyEx = 0;
        $this->amountMentEx = 0;
        $this->amountWbEx = 0;
        $this->scheduledEventsWordCount = 0;
        $this->nonScheduledEventsWordCount = 0;
        $this->scheduledEventsCharacterCount = 0;
        $this->nonScheduledEventsCharacterCount = 0;
        $this->functZonesWordCount = 0;
        $this->ltGoalsWordCount = 0;
        $this->userNotesWordCount = 0;
        $this->functZonesCharacterCount = 0;
        $this->ltGoalsCharacterCount = 0;
        $this->userNotesCharacterCount = 0;
        $this->wbJournalWordCount = 0;
        $this->wbJournalCharacterCount = 0;
    }

    /**
     * @return mixed
     */
    public function getSumNumEvents()
    {
        return $this->scheduledEvents + $this->nonScheduledEvents;
    }

    /**
     * @return mixed
     */
    public function getSumHealthTrackEvents()
    {
        return $this->phyExEvents + $this->mentExEvents + $this->wbExEvents;
    }

    /**
     * @return mixed
     */
    public function getSumCompletedEvents()
    {
        return $this->completedScheduledEvents + $this->completedNonScheduledEvents;
    }

    /**
     * @return mixed
     */
    public function getSumCompletedHealthTrackEvents()
    {
        return $this->completedPhyExEvents + $this->completedMentExEvents + $this->completedWbExEvents;
    }

    /**
     * @return mixed
     */
    public function getSumWordCount()
    {
        return $this->scheduledEventsWordCount + $this->nonScheduledEventsWordCount;
    }

    /**
     * @return mixed
     */
    public function getSumEventsCharacterCount()
    {
        return $this->scheduledEventsCharacterCount + $this->nonScheduledEventsCharacterCount;
    }

    /**
     * @return mixed
     */
    public function getSumWordCountNotes()
    {
        return $this->functZonesWordCount + $this->ltGoalsWordCount + $this->userNotesWordCount;
    }

    /**
     * @return mixed
     */
    public function getSumCharacterCountNotes()
    {
        return $this->functZonesCharacterCount + $this->ltGoalsCharacterCount + $this->userNotesCharacterCount;
    }



    /**
     * @return mixed
     */
    public function getScheduledEvents()
    {
        return $this->scheduledEvents;
    }

    /**
     * @param mixed $scheduledEvents
     */
    public function setScheduledEvents($scheduledEvents): void
    {
        $this->scheduledEvents = $scheduledEvents;
    }

    /**
     * @return mixed
     */
    public function getNonScheduledEvents()
    {
        return $this->nonScheduledEvents;
    }

    /**
     * @param mixed $nonScheduledEvents
     */
    public function setNonScheduledEvents($nonScheduledEvents): void
    {
        $this->nonScheduledEvents = $nonScheduledEvents;
    }

    /**
     * @return mixed
     */
    public function getHighPriorityEvents()
    {
        return $this->highPriorityEvents;
    }

    /**
     * @param mixed $highPriorityEvents
     */
    public function setHighPriorityEvents($highPriorityEvents): void
    {
        $this->highPriorityEvents = $highPriorityEvents;
    }

    /**
     * @return mixed
     */
    public function getRepeatedEvents()
    {
        return $this->repeatedEvents;
    }

    /**
     * @param mixed $repeatedEvents
     */
    public function setRepeatedEvents($repeatedEvents): void
    {
        $this->repeatedEvents = $repeatedEvents;
    }

    /**
     * @return mixed
     */
    public function getPhyExEvents()
    {
        return $this->phyExEvents;
    }

    /**
     * @param mixed $phyExEvents
     */
    public function setPhyExEvents($phyExEvents): void
    {
        $this->phyExEvents = $phyExEvents;
    }

    /**
     * @return mixed
     */
    public function getMentExEvents()
    {
        return $this->mentExEvents;
    }

    /**
     * @param mixed $mentExEvents
     */
    public function setMentExEvents($mentExEvents): void
    {
        $this->mentExEvents = $mentExEvents;
    }

    /**
     * @return mixed
     */
    public function getWbExEvents()
    {
        return $this->wbExEvents;
    }

    /**
     * @param mixed $wbExEvents
     */
    public function setWbExEvents($wbExEvents): void
    {
        $this->wbExEvents = $wbExEvents;
    }

    /**
     * @return mixed
     */
    public function getCompletedScheduledEvents()
    {
        return $this->completedScheduledEvents;
    }

    /**
     * @param mixed $completedScheduledEvents
     */
    public function setCompletedScheduledEvents($completedScheduledEvents): void
    {
        $this->completedScheduledEvents = $completedScheduledEvents;
    }

    /**
     * @return mixed
     */
    public function getCompletedNonScheduledEvents()
    {
        return $this->completedNonScheduledEvents;
    }

    /**
     * @param mixed $completedNonScheduledEvents
     */
    public function setCompletedNonScheduledEvents($completedNonScheduledEvents): void
    {
        $this->completedNonScheduledEvents = $completedNonScheduledEvents;
    }

    /**
     * @return mixed
     */
    public function getCompletedHighPriorityEvents()
    {
        return $this->completedHighPriorityEvents;
    }

    /**
     * @param mixed $completedHighPriorityEvents
     */
    public function setCompletedHighPriorityEvents($completedHighPriorityEvents): void
    {
        $this->completedHighPriorityEvents = $completedHighPriorityEvents;
    }

    /**
     * @return mixed
     */
    public function getCompletedRepeatEvents()
    {
        return $this->completedRepeatEvents;
    }

    /**
     * @param mixed $completedRepeatEvents
     */
    public function setCompletedRepeatEvents($completedRepeatEvents): void
    {
        $this->completedRepeatEvents = $completedRepeatEvents;
    }

    /**
     * @return mixed
     */
    public function getCompletedPhyExEvents()
    {
        return $this->completedPhyExEvents;
    }

    /**
     * @param mixed $completedPhyExEvents
     */
    public function setCompletedPhyExEvents($completedPhyExEvents): void
    {
        $this->completedPhyExEvents = $completedPhyExEvents;
    }

    /**
     * @return mixed
     */
    public function getCompletedMentExEvents()
    {
        return $this->completedMentExEvents;
    }

    /**
     * @param mixed $completedMentExEvents
     */
    public function setCompletedMentExEvents($completedMentExEvents): void
    {
        $this->completedMentExEvents = $completedMentExEvents;
    }

    /**
     * @return mixed
     */
    public function getCompletedWbExEvents()
    {
        return $this->completedWbExEvents;
    }

    /**
     * @param mixed $completedWbExEvents
     */
    public function setCompletedWbExEvents($completedWbExEvents): void
    {
        $this->completedWbExEvents = $completedWbExEvents;
    }

    /**
     * @return mixed
     */
    public function getNumTotalFolders()
    {
        return $this->numTotalFolders;
    }

    /**
     * @param mixed $numTotalFolders
     */
    public function setNumTotalFolders($numTotalFolders): void
    {
        $this->numTotalFolders = $numTotalFolders;
    }

    /**
     * @return mixed
     */
    public function getNumTotalNotes()
    {
        return $this->numTotalNotes;
    }

    /**
     * @param mixed $numTotalNotes
     */
    public function setNumTotalNotes($numTotalNotes): void
    {
        $this->numTotalNotes = $numTotalNotes;
    }

    /**
     * @return mixed
     */
    public function getNumItemsInCalendar()
    {
        return $this->numItemsInCalendar;
    }

    /**
     * @param mixed $numItemsInCalendar
     */
    public function setNumItemsInCalendar($numItemsInCalendar): void
    {
        $this->numItemsInCalendar = $numItemsInCalendar;
    }

    /**
     * @return mixed
     */
    public function getHiddenEventsCount()
    {
        return $this->hiddenEventsCount;
    }

    /**
     * @param mixed $hiddenEventsCount
     */
    public function setHiddenEventsCount($hiddenEventsCount): void
    {
        $this->hiddenEventsCount = $hiddenEventsCount;
    }

    /**
     * @return mixed
     */
    public function getAmountPhyEx()
    {
        return $this->amountPhyEx;
    }

    /**
     * @param mixed $amountPhyEx
     */
    public function setAmountPhyEx($amountPhyEx): void
    {
        $this->amountPhyEx = $amountPhyEx;
    }

    /**
     * @return mixed
     */
    public function getAmountMentEx()
    {
        return $this->amountMentEx;
    }

    /**
     * @param mixed $amountMentEx
     */
    public function setAmountMentEx($amountMentEx): void
    {
        $this->amountMentEx = $amountMentEx;
    }

    /**
     * @return mixed
     */
    public function getAmountWbEx()
    {
        return $this->amountWbEx;
    }

    /**
     * @param mixed $amountWbEx
     */
    public function setAmountWbEx($amountWbEx): void
    {
        $this->amountWbEx = $amountWbEx;
    }

    /**
     * @return mixed
     */
    public function getScheduledEventsWordCount()
    {
        return $this->scheduledEventsWordCount;
    }

    /**
     * @param mixed $scheduledEventsWordCount
     */
    public function setScheduledEventsWordCount($scheduledEventsWordCount): void
    {
        $this->scheduledEventsWordCount = $scheduledEventsWordCount;
    }

    /**
     * @return mixed
     */
    public function getNonScheduledEventsWordCount()
    {
        return $this->nonScheduledEventsWordCount;
    }

    /**
     * @param mixed $nonScheduledEventsWordCount
     */
    public function setNonScheduledEventsWordCount($nonScheduledEventsWordCount): void
    {
        $this->nonScheduledEventsWordCount = $nonScheduledEventsWordCount;
    }

    /**
     * @return mixed
     */
    public function getScheduledEventsCharacterCount()
    {
        return $this->scheduledEventsCharacterCount;
    }

    /**
     * @param mixed $scheduledEventsCharacterCount
     */
    public function setScheduledEventsCharacterCount($scheduledEventsCharacterCount): void
    {
        $this->scheduledEventsCharacterCount = $scheduledEventsCharacterCount;
    }

    /**
     * @return mixed
     */
    public function getNonScheduledEventsCharacterCount()
    {
        return $this->nonScheduledEventsCharacterCount;
    }

    /**
     * @param mixed $nonScheduledEventsCharacterCount
     */
    public function setNonScheduledEventsCharacterCount($nonScheduledEventsCharacterCount): void
    {
        $this->nonScheduledEventsCharacterCount = $nonScheduledEventsCharacterCount;
    }

    /**
     * @return mixed
     */
    public function getFunctZonesWordCount()
    {
        return $this->functZonesWordCount;
    }

    /**
     * @param mixed $functZonesWordCount
     */
    public function setFunctZonesWordCount($functZonesWordCount): void
    {
        $this->functZonesWordCount = $functZonesWordCount;
    }

    /**
     * @return mixed
     */
    public function getLtGoalsWordCount()
    {
        return $this->ltGoalsWordCount;
    }

    /**
     * @param mixed $ltGoalsWordCount
     */
    public function setLtGoalsWordCount($ltGoalsWordCount): void
    {
        $this->ltGoalsWordCount = $ltGoalsWordCount;
    }

    /**
     * @return mixed
     */
    public function getUserNotesWordCount()
    {
        return $this->userNotesWordCount;
    }

    /**
     * @param mixed $userNotesWordCount
     */
    public function setUserNotesWordCount($userNotesWordCount): void
    {
        $this->userNotesWordCount = $userNotesWordCount;
    }

    /**
     * @return mixed
     */
    public function getFunctZonesCharacterCount()
    {
        return $this->functZonesCharacterCount;
    }

    /**
     * @param mixed $functZonesCharacterCount
     */
    public function setFunctZonesCharacterCount($functZonesCharacterCount): void
    {
        $this->functZonesCharacterCount = $functZonesCharacterCount;
    }

    /**
     * @return mixed
     */
    public function getLtGoalsCharacterCount()
    {
        return $this->ltGoalsCharacterCount;
    }

    /**
     * @param mixed $ltGoalsCharacterCount
     */
    public function setLtGoalsCharacterCount($ltGoalsCharacterCount): void
    {
        $this->ltGoalsCharacterCount = $ltGoalsCharacterCount;
    }

    /**
     * @return mixed
     */
    public function getUserNotesCharacterCount()
    {
        return $this->userNotesCharacterCount;
    }

    /**
     * @param mixed $userNotesCharacterCount
     */
    public function setUserNotesCharacterCount($userNotesCharacterCount): void
    {
        $this->userNotesCharacterCount = $userNotesCharacterCount;
    }

    /**
     * @return mixed
     */
    public function getWbJournalWordCount()
    {
        return $this->wbJournalWordCount;
    }

    /**
     * @param mixed $wbJournalWordCount
     */
    public function setWbJournalWordCount($wbJournalWordCount): void
    {
        $this->wbJournalWordCount = $wbJournalWordCount;
    }

    /**
     * @return mixed
     */
    public function getWbJournalCharacterCount()
    {
        return $this->wbJournalCharacterCount;
    }

    /**
     * @param mixed $wbJournalCharacterCount
     */
    public function setWbJournalCharacterCount($wbJournalCharacterCount): void
    {
        $this->wbJournalCharacterCount = $wbJournalCharacterCount;
    }

}
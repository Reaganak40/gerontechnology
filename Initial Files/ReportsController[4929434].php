<?php

namespace App\Controller;

use App\Entity\Entry;
use App\Entity\Event;
use App\Entity\StaticEntries;
use App\Entity\SummaryReport;
use App\Report\ReportService;
use App\Repository\EntryRepository;
use App\Repository\EventRepository;
use App\Repository\InteractionRepository;
use App\Repository\UserRepository;
use App\Utility\DateRange;
use DateTime;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Knp\Bundle\SnappyBundle\Snappy\Response\PdfResponse;

/**
 * Class ReportsController
 * @package App\Controller
 * @Route("/reports")
 */
class ReportsController extends AbstractController
{
    /**
     * @Route("/interactions", name="interactions_user_list")
     * @param UserRepository $userRepository
     * @return Response
     */
    public function interactionUserList(UserRepository $userRepository)
    {
        $users = $userRepository->findBy(array('deactivated' => null));

        return $this->render('reports/interaction_user_list.html.twig',
            array(
                'users' => $users
            ));
    }

    /**
     * @Route("/interactions/{userId}", name="interactions_by_user")
     * @param UserRepository $userRepository
     * @param InteractionRepository $interactionRepository
     * @param int $userId
     * @return Response
     */
    public function interactionsByUser(UserRepository $userRepository, InteractionRepository $interactionRepository, int $userId): Response
    {
        $user = $userRepository->findOrException($userId);

        $interactions = $interactionRepository->findBy(array('user' => $userId));

        $doctrine = $this->getDoctrine();

        return $this->render('reports/interactions_by_user.html.twig',
            array(
                'user'          => $user,
                'interactions'  => $interactions,
                'doctrine'      => $doctrine
            ));
    }

    /**
     * @Route("/events/{userId}", name="events_by_user")
     * @param UserRepository $userRepository
     * @param EventRepository $eventRepository
     * @param int $userId
     * @return Response
     */
    public function eventsByUser(UserRepository $userRepository, EventRepository $eventRepository, int $userId): Response
    {
        $user = $userRepository->findOrException($userId);
        $events = $eventRepository->findBy(array('user' => $userId));

        return $this->render('reports/events_by_user.html.twig',
            array(
                'user'      => $user,
                'events'    => $events
            ));
    }

    /**
     * @Route("/summary-report-by-user/{userId}", name="summary_report_by_user")
     * @param UserRepository $userRepository
     * @param InteractionRepository $interactionRepository
     * @param EventRepository $eventRepository
     * @param int $userId
     */
    public function summaryReport(
        UserRepository $userRepository,
        EventRepository $eventRepository,
        EntryRepository $entryRepository,
        ReportService $reportService,
        int $userId)
    {
        $user = $userRepository->findOrException($userId);
        $events = $eventRepository->findBy(array('user' => $userId), array('eventToken' => 'ASC'));
        $entries = $entryRepository->findBy(array('user' => $userId), array('entryToken' => 'ASC'));

        //totals from the weekly graphs
        $range = DateRange::weekFromDateTime(new DateTime());
        $start = $range->getStart();
        $end = $range->getEnd();

        $physicalTotal = $reportService->physicalExerciseReport($user, $start, $end)->getTotal();
        $mentalTotal = $reportService->mentalExerciseReport($user, $start, $end)->getTotal();
        $wellbeingTotal = $reportService->wellbeingExerciseReport($user, $start, $end)->getTotal();

        $summaryReport = new SummaryReport();
        $dotCount = $this->getCalendarDotCount($entries);

        $summaryReport = $this->getEventsData($events, $summaryReport);
        $summaryReport = $this->getEntriesData($entries, $summaryReport);

        return $this->render('reports/summary_report_by_user.html.twig',
            array(
                'user'              => $user,
                'summaryReport'     => $summaryReport,
                'physicalTotal'     => $physicalTotal,
                'mentalTotal'       => $mentalTotal,
                'wellbeingTotal'    => $wellbeingTotal,
                'dotCount'          => $dotCount,
            ));
    }


    /**
     * @Route("/pdf-summary-report-by-user/{userId}", name="pdf_summary_report_by_user")
     * @param UserRepository $userRepository
     * @param InteractionRepository $interactionRepository
     * @param EventRepository $eventRepository
     * @param int $userId
     */
    public function summaryReportPdf(
        UserRepository $userRepository,
        EventRepository $eventRepository,
        EntryRepository $entryRepository,
        ReportService $reportService,
        \Knp\Snappy\Pdf $knpSnappyPdf,
        int $userId)
    {
        $user = $userRepository->findOrException($userId);
        $events = $eventRepository->findBy(array('user' => $userId), array('eventToken' => 'ASC'));
        $entries = $entryRepository->findBy(array('user' => $userId), array('entryToken' => 'ASC'));

        //totals from the weekly graphs
        $range = DateRange::weekFromDateTime(new DateTime());
        $start = $range->getStart();
        $end = $range->getEnd();

        $physicalTotal = $reportService->physicalExerciseReport($user, $start, $end)->getTotal();
        $mentalTotal = $reportService->mentalExerciseReport($user, $start, $end)->getTotal();
        $wellbeingTotal = $reportService->wellbeingExerciseReport($user, $start, $end)->getTotal();

        $summaryReport = new SummaryReport();
        $dotCount = $this->getCalendarDotCount($entries);

        $summaryReport = $this->getEventsData($events, $summaryReport);
        $summaryReport = $this->getEntriesData($entries, $summaryReport);

        $date = new DateTime();
        $dateTime = $date->format('Y-m-d H:i:s');

        return new PdfResponse(
            $knpSnappyPdf->getOutputFromHtml(
                $this->renderView(
                    'pdf/pdf_summary_report_by_user.html.twig',
                    array(
                        'user'              => $user,
                        'summaryReport'     => $summaryReport,
                        'physicalTotal'     => $physicalTotal,
                        'mentalTotal'       => $mentalTotal,
                        'wellbeingTotal'    => $wellbeingTotal,
                        'dotCount'          => $dotCount,
                    )
                ),
                array(
                    'lowquality' => false,
                    'encoding' => 'utf-8',
                    'page-size' => 'Letter',
                    'images' => true,
                    'image-quality' => 100,
                    'orientation' => 'Portrait',
                )
            ),
            $user->getUserIdentifier() . " - " . $dateTime . ' - Summary Report.pdf'
        );

    }

    /**
     * @param $events
     * @param SummaryReport $summaryReport
     * @return SummaryReport
     */
    private function getEventsData($events, SummaryReport $summaryReport): SummaryReport
    {
        $today = new \DateTime('now');
        $lastToken = '';

        foreach ($events as $event) {
            // only dealing with events on today's date
            if (($event->getEventDate()->format('Y-m-d') == $today->format('Y-m-d')) && $event->getAction() != Event::ACTION_DELETE) {

                // only taking into account the first instance of an event
                if ($lastToken != $event->getEventToken()) {
                    // scheduled events
                    if ($event->getNoSpecifiedTime() == 0) {
                        $summaryReport->setScheduledEvents($summaryReport->getScheduledEvents() + 1);
                    }

                    // non-scheduled events
                    if ($event->getNoSpecifiedTime() == 1) {
                        $summaryReport->setNonScheduledEvents($summaryReport->getNonScheduledEvents() + 1);
                    }

                    // high priority
                    if ($event->getPriority() == 1) {
                        $summaryReport->setHighPriorityEvents($summaryReport->getHighPriorityEvents() + 1);
                    }

                    // repeated events
                    if ($event->isRecurring()) {
                        $summaryReport->setRepeatedEvents($summaryReport->getRepeatedEvents() + 1);
                    }

                    // physical exercise events
                    if ($event->getHealthTrackType() == Event::TRACK_TYPE_PHYSICAL) {
                        $summaryReport->setPhyExEvents($summaryReport->getPhyExEvents() + 1);
                    }

                    // mental exercise events
                    if ($event->getHealthTrackType() == Event::TRACK_TYPE_MENTAL) {
                        $summaryReport->setMentExEvents($summaryReport->getMentExEvents() + 1);
                    }

                    // well-being exercise events
                    if ($event->getHealthTrackType() == Event::TRACK_TYPE_WELLBEING) {
                        $summaryReport->setWbExEvents($summaryReport->getWbExEvents() + 1);
                    }

                    // number of items in calendar
                    if (($event->getEventType() == Event::TYPE_SCHEDULED) && ($event->getRecurringHide() == 0)) {
                        $summaryReport->setNumItemsInCalendar($summaryReport->getNumItemsInCalendar() + 1);
                    }

                    // hidden events count
                    if (($event->getEventType() == Event::TYPE_SCHEDULED) && ($event->getRecurringHide() == 1)) {
                        $summaryReport->setHiddenEventsCount($summaryReport->getHiddenEventsCount() + 1);
                    }

                }

                // scheduled events & word/character count
                if ($event->getNoSpecifiedTime() == 0) {
                    $summaryReport->setScheduledEventsWordCount(
                        $summaryReport->getScheduledEventsWordCount() +
                        str_word_count($event->getTaskTitle()) +
                        str_word_count($event->getTaskDescription()));

                    $summaryReport->setScheduledEventsCharacterCount(
                        $summaryReport->getScheduledEventsCharacterCount() +
                        strlen($event->getTaskTitle()) +
                        strlen($event->getTaskDescription()));
                }

                // non-scheduled events and word/character count
                if ($event->getNoSpecifiedTime() == 1) {
                    $summaryReport->setNonScheduledEventsWordCount(
                        $summaryReport->getNonScheduledEventsWordCount() +
                        str_word_count($event->getTaskTitle()) +
                        str_word_count($event->getTaskDescription()));

                    $summaryReport->setNonScheduledEventsCharacterCount(
                        $summaryReport->getNonScheduledEventsCharacterCount() +
                        strlen($event->getTaskTitle()) +
                        strlen($event->getTaskDescription()));

                }

                /** completed events need to be outside the token limitation, or it won't get to where the completed
                    events are stored, the same is true of the exercise counts **/
                // completed scheduled events
                if (($event->isCompleted()) && ($event->getNoSpecifiedTime() == 0)) {
                    $summaryReport->setCompletedScheduledEvents($summaryReport->getCompletedScheduledEvents() + 1);
                }

                // completed non-scheduled events
                if (($event->isCompleted()) && ($event->getNoSpecifiedTime() == 1)) {
                    $summaryReport->setCompletedNonScheduledEvents($summaryReport->getCompletedNonScheduledEvents() + 1);
                }

                // completed high priority events
                if (($event->isCompleted()) && ($event->getPriority() == 1)) {
                    $summaryReport->setCompletedHighPriorityEvents($summaryReport->getCompletedHighPriorityEvents() + 1);
                }

                // completed repeated events
                if (($event->isCompleted()) && ($event->isRecurring())) {
                    $summaryReport->setCompletedRepeatEvents($summaryReport->getCompletedRepeatEvents() + 1);
                }

                // completed physical exercise events
                if (($event->isCompleted()) && ($event->getHealthTrackType() == Event::TRACK_TYPE_PHYSICAL)) {
                    $summaryReport->setCompletedPhyExEvents($summaryReport->getCompletedPhyExEvents() + 1);
                }

                // completed mental exercise events
                if (($event->isCompleted()) && ($event->getHealthTrackType() == Event::TRACK_TYPE_MENTAL)) {
                    $summaryReport->setCompletedMentExEvents($summaryReport->getCompletedMentExEvents() + 1);
                }

                // completed well-being exercise events
                if (($event->isCompleted()) && ($event->getHealthTrackType() == Event::TRACK_TYPE_WELLBEING)) {
                    $summaryReport->setCompletedWbExEvents($summaryReport->getCompletedWbExEvents() + 1);
                }

                // physical exercise minutes
                if ($event->getHealthTrackType() == Event::TRACK_TYPE_PHYSICAL) {
                    if ($event->getAction() != Event::ACTION_DELETE) {
                        $summaryReport->setAmountPhyEx($summaryReport->getAmountPhyEx() + $event->getHealthTrackDataInt());
                    }
                }

                // mental exercise instances
                if ($event->getHealthTrackType() == Event::TRACK_TYPE_MENTAL) {
                    $summaryReport->setAmountMentEx($summaryReport->getAmountMentEx() + $event->getHealthTrackDataInt());
                }

                // well-being exercise instances
                if ($event->getHealthTrackType() == Event::TRACK_TYPE_WELLBEING) {
                    $summaryReport->setAmountWbEx($summaryReport->getAmountWbEx() + $event->getHealthTrackDataInt());
                }

                $lastToken = $event->getEventToken();
            }
        }

        return $summaryReport;
    }

    /**
     * @param $entries
     * @param SummaryReport $summaryReport
     * @return SummaryReport
     */
    private function getEntriesData($entries, SummaryReport $summaryReport): SummaryReport
    {
        $today = new \DateTime('now');
        $lastToken = '';

        foreach ($entries as $entry) {
            if ($entry->getTimestampLocal()->format('Y-m-d') == $today->format('Y-m-d') && $entry->getAction() != Entry::ACTION_DELETE) {

                // we only want the first instance of an entry to count for folder and note counts but not word and character counts
                if ($lastToken != $entry->getEntryToken()) {
                    // folder count
                    if ($entry->getEntryType() == Entry::TYPE_FOLDER) {
                        $summaryReport->setNumTotalFolders($summaryReport->getNumTotalFolders() + 1);
                    }

                    // note count
                    if ($entry->getEntryType() == Entry::TYPE_NOTE) {
                        $summaryReport->setNumTotalNotes($summaryReport->getNumTotalNotes() + 1);
                    }
                }

                // note word & character counts
                if ($entry->getEntryType() == Entry::TYPE_NOTE) {
                    // functional zones word/character count
                    if ($entry->getFolderEntryId() == StaticEntries::ENTRY_TYPE_FUNCTIONAL_ZONES) {
                        $summaryReport->setFunctZonesWordCount(
                            $summaryReport->getFunctZonesWordCount() +
                            str_word_count($entry->getTitle()) +
                            str_word_count($entry->getContent()));

                        $summaryReport->setFunctZonesCharacterCount(
                            $summaryReport->getFunctZonesCharacterCount() +
                            strlen($entry->getTitle()) +
                            strlen($entry->getContent()));

                    } // long term goals word/character count
                    elseif ($entry->getFolderEntryId() == StaticEntries::ENTRY_TYPE_LONG_TERM_GOALS) {
                        $summaryReport->setLtGoalsWordCount(
                            $summaryReport->getLtGoalsWordCount() +
                            str_word_count($entry->getTitle()) +
                            str_word_count($entry->getContent()));

                        $summaryReport->setLtGoalsCharacterCount(
                            $summaryReport->getLtGoalsCharacterCount() +
                            strlen($entry->getTitle()) +
                            strlen($entry->getContent()));
                    } // exclude entry types for Gratitude, Acts Of Kindness, Positive Daily Events and Mindfulness
                    elseif ($entry->getFolderEntryId() != StaticEntries::ENTRY_TYPE_GRATITUDE &&
                        $entry->getFolderEntryId() != StaticEntries::ENTRY_TYPE_ACTS_OF_KINDNESS &&
                        $entry->getFolderEntryId() != StaticEntries::ENTRY_TYPE_POSITIVE_DAILY_EVENTS &&
                        $entry->getFolderEntryId() != StaticEntries::ENTRY_TYPE_MINDFULNESS) {

                        $summaryReport->setUserNotesWordCount(
                            $summaryReport->getUserNotesWordCount() +
                            str_word_count($entry->getTitle()) +
                            str_word_count($entry->getContent()));

                        $summaryReport->setUserNotesCharacterCount(
                            $summaryReport->getUserNotesCharacterCount() +
                            strlen($entry->getTitle()) +
                            strlen($entry->getContent()));
                    }
                    // Well-Being Journal Word Count
                    if ($entry->getFolderEntryId() == StaticEntries::ENTRY_TYPE_GRATITUDE ||
                        $entry->getFolderEntryId() == StaticEntries::ENTRY_TYPE_ACTS_OF_KINDNESS ||
                        $entry->getFolderEntryId() == StaticEntries::ENTRY_TYPE_POSITIVE_DAILY_EVENTS ||
                        $entry->getFolderEntryId() == StaticEntries::ENTRY_TYPE_MINDFULNESS) {

                        $summaryReport->setWbJournalWordCount(
                            $summaryReport->getWbJournalWordCount() +
                            str_word_count($entry->getTitle()) +
                            str_word_count($entry->getContent()));

                        $summaryReport->setWbJournalCharacterCount(
                            $summaryReport->getWbJournalCharacterCount() +
                            strlen($entry->getTitle()) +
                            strlen($entry->getContent()));
                    }
                }

                $lastToken = $entry->getEntryToken();
            }
        }

        return $summaryReport;
    }

    /**
     * @param $entries
     * @return int
     */
    private function getCalendarDotCount($entries): int
    {
        $today = new \DateTime('now');
        $dotCount = 0;

        for ($x = 1; $x <= 31; $x++) {
            foreach($entries as $entry) {
                if ($entry->getTimestampLocal()->format('m') == $today->format('m') && $entry->getTimestampLocal()->format('d') == $x) {
                    $dotCount++;
                    break;
                }
            }
        }

        return $dotCount;
    }

}
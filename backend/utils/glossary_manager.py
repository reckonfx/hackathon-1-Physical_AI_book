from typing import Dict, List, Optional, Tuple
import re
from backend.config import TECHNICAL_TERMS_LIST


class GlossaryManager:
    """
    Manager for technical terminology and glossary references.
    """

    def __init__(self, terms_list: List[str] = None):
        self.terms_list = terms_list or TECHNICAL_TERMS_LIST
        # Create a mapping for quick lookup and case-insensitive matching
        self.terms_map = {term.lower(): term for term in self.terms_list}

    def identify_technical_terms(self, text: str) -> List[str]:
        """
        Identify technical terms in the provided text.

        Args:
            text: Input text to analyze

        Returns:
            List of technical terms found in the text
        """
        found_terms = set()

        for term in self.terms_map.keys():
            # Use word boundaries to match exact terms, case-insensitive
            pattern = r'\b' + re.escape(term) + r'\b'
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Use the original case from our terms list
                original_case = self.terms_map[term.lower()]
                found_terms.add(original_case)

        return list(found_terms)

    def extract_terms_with_context(self, text: str, context_window: int = 10) -> List[Dict[str, str]]:
        """
        Extract technical terms with their surrounding context.

        Args:
            text: Input text to analyze
            context_window: Number of characters before/after the term to include

        Returns:
            List of dictionaries with term and context
        """
        terms_with_context = []

        for term in self.terms_map.keys():
            pattern = r'\b(' + re.escape(term) + r')\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                start_pos = match.start()
                end_pos = match.end()

                # Extract context
                context_start = max(0, start_pos - context_window)
                context_end = min(len(text), end_pos + context_window)
                context = text[context_start:context_end]

                original_case = self.terms_map[term.lower()]
                terms_with_context.append({
                    "term": original_case,
                    "context": context,
                    "position": start_pos
                })

        return terms_with_context

    def get_glossary_definition(self, term: str) -> Optional[str]:
        """
        Get the definition for a technical term.

        Args:
            term: Technical term to define

        Returns:
            Definition of the term or None if not found
        """
        term_lower = term.lower()
        if term_lower in self.terms_map:
            # In a real implementation, this would fetch from a glossary database
            definitions = {
                "slam": "Simultaneous Localization and Mapping - a computational problem of constructing or updating a map of an unknown environment while simultaneously keeping track of an agent's location within it.",
                "ros": "Robot Operating System - a flexible framework for writing robot software.",
                "gazebo": "A 3D simulation environment for autonomous robots.",
                "isaac": "NVIDIA Isaac - a robotics platform for developing and deploying AI-based applications.",
                "vla": "Vision-Language-Action model - a type of AI model that combines visual, linguistic, and action capabilities.",
                "ai": "Artificial Intelligence - intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals.",
                "ml": "Machine Learning - the study of computer algorithms that can improve automatically through experience and data.",
                "nn": "Neural Network - a series of algorithms that endeavors to recognize underlying relationships in a set of data through a process that mimics how the human brain operates.",
                "cnn": "Convolutional Neural Network - a class of deep neural networks used for analyzing visual imagery.",
                "rnn": "Recurrent Neural Network - a class of artificial neural networks where connections between nodes form a directed graph along a temporal sequence.",
                "lstm": "Long Short-Term Memory - a type of recurrent neural network that can learn long-term dependencies.",
                "transformer": "A deep learning model that uses self-attention mechanisms to process sequential data.",
                "pid": "Proportional-Integral-Derivative controller - a control loop mechanism employing feedback.",
                "pid controller": "Proportional-Integral-Derivative controller - a control loop mechanism employing feedback.",
                "kinematics": "The branch of mechanics concerned with the motion of objects without reference to force.",
                "dynamics": "The branch of mechanics concerned with the motion of bodies under the action of forces.",
                "forward kinematics": "The use of kinematic equations to compute the position of the end-effector from specified values of joint parameters.",
                "inverse kinematics": "The use of kinematic equations to determine the joint parameters that achieve a specified position of the end-effector.",
                "end-effector": "The device at the end of a robotic arm designed to interact with the environment.",
                "workspace": "The space in which the robot can operate.",
                "degrees of freedom": "The number of parameters that define the configuration of a mechanical system.",
                "dof": "Degrees of Freedom - the number of parameters that define the configuration of a mechanical system.",
                "actuator": "A component of a machine that causes movement.",
                "sensor": "A device that detects or measures a physical property and records, indicates, or otherwise responds to it.",
                "lidar": "Light Detection and Ranging - a remote sensing method that uses light in the form of a pulsed laser.",
                "imu": "Inertial Measurement Unit - an electronic device that measures and reports a body's specific force, angular rate, and sometimes the magnetic field surrounding the body.",
                "computer vision": "An interdisciplinary scientific field that deals with how computers can gain high-level understanding from digital images or videos.",
                "path planning": "The computational problem of finding a valid sequence of configurations to move an object from a source to a destination.",
                "motion planning": "The computational problem of finding a valid sequence of configurations to move an object from a source to a destination.",
                "control theory": "An interdisciplinary branch of engineering and mathematics that deals with the behavior of dynamical systems with inputs.",
                "feedback control": "A control system that uses the difference between the desired output and the actual output to adjust the input.",
                "state estimation": "The process of estimating the state of a system from measurements.",
                "kalman filter": "An algorithm that uses a series of measurements observed over time to estimate the unknown variables.",
                "particle filter": "A set of algorithms for estimating the state of a system using a collection of particles.",
                "reinforcement learning": "An area of machine learning concerned with how software agents ought to take actions in an environment to maximize cumulative reward.",
                "deep learning": "A subset of machine learning based on artificial neural networks with representation learning.",
                "neural network": "A series of algorithms that endeavors to recognize underlying relationships in a set of data through a process that mimics how the human brain operates.",
                "robotics": "The interdisciplinary sector of science and engineering dedicated to creating machines that assist humans.",
                "embodied ai": "Artificial intelligence systems that interact with the physical world through a body or form.",
                "physical ai": "Artificial intelligence focused on understanding and interacting with the physical world.",
                "humanoid": "A robot or other device with a human-like body structure.",
                "manipulation": "The ability of a robot to physically interact with objects in its environment.",
                "locomotion": "The ability of a robot to move from one place to another.",
                "navigation": "The ability of a robot to move through an environment from a source to a destination.",
                "localization": "The process of determining the robot's position and orientation in an environment.",
                "mapping": "The process of creating a representation of the environment for navigation purposes.",
                "autonomous": "Operating independently without external control.",
                "autonomy": "The degree to which a system can operate without human intervention.",
            }
            return definitions.get(term_lower)

    def preserve_and_annotate_terms(self, text: str) -> Tuple[str, List[Dict[str, str]]]:
        """
        Annotate technical terms in the text while preserving them.

        Args:
            text: Input text to process

        Returns:
            Tuple of (annotated text, list of term annotations)
        """
        annotations = []
        terms_found = self.identify_technical_terms(text)

        annotated_text = text
        for term in terms_found:
            # Create an annotation for each occurrence
            pattern = r'\b(' + re.escape(term) + r')\b'
            for match in re.finditer(pattern, annotated_text, re.IGNORECASE):
                annotations.append({
                    "term": term,
                    "definition": self.get_glossary_definition(term),
                    "position": match.start()
                })

        return annotated_text, annotations


# Global glossary manager instance
glossary_manager = GlossaryManager()